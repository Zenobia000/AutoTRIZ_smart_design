"""Unified TRIZ solve service — orchestrates classify → route → solve across 3 paths."""

import json
import logging

from sqlalchemy.orm import Session

from src.models.contradiction import Contradiction
from src.models.triz import TrizSolution
from src.models.separation_solution import SeparationSolution
from src.models.sufield_solution import SuFieldSolution
from src.services.llm_service import llm_service
from src.services.triz_engine import triz_engine

logger = logging.getLogger(__name__)


class TrizSolveService:

    def solve(self, contradiction: Contradiction, constraints: str, db: Session) -> dict:
        """Run unified 3-path TRIZ solve for a single contradiction."""

        # Step 1: Classify
        classification = self._classify(contradiction)
        types = classification.get("types", [])

        contradiction.contradiction_types = types
        contradiction.sufield_state = classification.get("sufield_state") or ""

        param_mapping = None
        matrix_lookup = None
        tc_solutions = []
        sep_solutions = []
        sf_solutions = []

        # Step 2: Path A — Technical Contradiction
        if "technical" in types:
            param_mapping = self._map_params(contradiction)
            if param_mapping:
                imp_list = param_mapping.get("improve_params", [])
                wor_list = param_mapping.get("worsen_params", [])
                if imp_list and wor_list:
                    imp_id = imp_list[0]["triz_id"]
                    wor_id = wor_list[0]["triz_id"]
                    contradiction.improve_param_id = imp_id
                    contradiction.worsen_param_id = wor_id

                    matrix_lookup = triz_engine.lookup_matrix(imp_id, wor_id)

                    # If matrix has no entry, try second candidate pair
                    if not matrix_lookup and len(imp_list) > 1:
                        alt_id = imp_list[1]["triz_id"]
                        matrix_lookup = triz_engine.lookup_matrix(alt_id, wor_id)
                        if matrix_lookup:
                            imp_id = alt_id
                            contradiction.improve_param_id = imp_id

                    if matrix_lookup:
                        tc_solutions = self._solve_technical(
                            contradiction, constraints, imp_id, wor_id, matrix_lookup
                        )

        # Step 3: Path B — Physical Contradiction
        if "physical" in types and contradiction.physical_contradiction:
            sep_solutions = self._solve_physical(contradiction, constraints)

        # Step 4: Path C — Su-Field
        if "sufield" in types and contradiction.sufield_state:
            sf_solutions = self._solve_sufield(contradiction, constraints)

        # Persist
        for s in tc_solutions:
            db.add(s)
        for s in sep_solutions:
            db.add(s)
        for s in sf_solutions:
            db.add(s)
        db.commit()

        # Refresh for IDs
        for s in tc_solutions + sep_solutions + sf_solutions:
            db.refresh(s)

        return {
            "contradiction_id": contradiction.id,
            "classification": classification,
            "param_mapping": param_mapping,
            "matrix_lookup": matrix_lookup,
            "technical_solutions": tc_solutions,
            "separation_solutions": sep_solutions,
            "sufield_solutions": sf_solutions,
        }

    def _classify(self, c: Contradiction) -> dict:
        """Classify contradiction type(s) via LLM."""
        return llm_service.generate("triz_classify.md", {
            "code": c.code,
            "improve_param": c.improve_param,
            "worsen_param": c.worsen_param,
            "engineering_desc": c.engineering_desc,
            "physical_contradiction": c.physical_contradiction or "（無）",
        })

    def _map_params(self, c: Contradiction) -> dict | None:
        """Map free-text params to TRIZ 39 param IDs via LLM."""
        try:
            return llm_service.generate("triz_param_mapping.md", {
                "param_table": triz_engine.format_params_for_prompt(),
                "mapping_hints": triz_engine.mapping_hints,
                "improve_param": c.improve_param,
                "worsen_param": c.worsen_param,
                "engineering_desc": c.engineering_desc,
            })
        except Exception as e:
            logger.warning(f"Param mapping failed: {e}")
            return None

    def _solve_technical(
        self, c: Contradiction, constraints: str,
        imp_id: int, wor_id: int, principle_ids: list[int],
    ) -> list[TrizSolution]:
        """Generate TC solutions grounded in matrix lookup results."""
        imp_name = triz_engine.params[imp_id].name_zh if imp_id in triz_engine.params else str(imp_id)
        wor_name = triz_engine.params[wor_id].name_zh if wor_id in triz_engine.params else str(wor_id)

        contradiction_text = (
            f"{c.code}: 若要提高「{c.improve_param}」，"
            f"則「{c.worsen_param}」會惡化。{c.engineering_desc}"
        )

        result = llm_service.generate("triz_tc_solve.md", {
            "improve_id": imp_id,
            "improve_name": imp_name,
            "worsen_id": wor_id,
            "worsen_name": wor_name,
            "recommended_ids": ", ".join(str(x) for x in principle_ids),
            "principle_details": triz_engine.format_principles_for_prompt(principle_ids),
            "contradiction": contradiction_text,
            "constraints": constraints,
        })

        solutions = []
        for item in (result if isinstance(result, list) else [result]):
            solutions.append(TrizSolution(
                project_id=c.project_id,
                contradiction_id=c.id,
                principle_number=item.get("principle_number", 0),
                principle_name=item.get("principle_name", ""),
                abstract_strategy=item.get("abstract_strategy", ""),
                engineering_mappings=item.get("engineering_mappings", []),
                cost_description=item.get("cost_description", ""),
                robust_estimate=item.get("robust_estimate", {}),
                experiment_desc=item.get("experiment_desc", ""),
            ))
        return solutions

    def _solve_physical(self, c: Contradiction, constraints: str) -> list[SeparationSolution]:
        """Generate PC solutions using separation principles."""
        contradiction_text = (
            f"{c.code}: 若要提高「{c.improve_param}」，"
            f"則「{c.worsen_param}」會惡化。{c.engineering_desc}"
        )

        result = llm_service.generate("triz_pc_solve.md", {
            "separation_kb": triz_engine.format_separations_for_prompt(),
            "physical_contradiction": c.physical_contradiction,
            "engineering_desc": c.engineering_desc,
            "constraints": constraints,
        })

        solutions = []
        for item in (result if isinstance(result, list) else [result]):
            solutions.append(SeparationSolution(
                project_id=c.project_id,
                contradiction_id=c.id,
                separation_type=item.get("separation_type", ""),
                separation_name=item.get("separation_name", ""),
                strategy=item.get("strategy", ""),
                engineering_mappings=item.get("engineering_mappings", []),
                cost_description=item.get("cost_description", ""),
                experiment_desc=item.get("experiment_desc", ""),
            ))
        return solutions

    def _solve_sufield(self, c: Contradiction, constraints: str) -> list[SuFieldSolution]:
        """Generate SF solutions using 76 standard solutions."""
        standards = triz_engine.get_standards_for_state(c.sufield_state)
        if not standards:
            return []

        contradiction_text = (
            f"{c.code}: 若要提高「{c.improve_param}」，"
            f"則「{c.worsen_param}」會惡化。{c.engineering_desc}"
        )

        result = llm_service.generate("triz_sf_solve.md", {
            "sufield_state": c.sufield_state,
            "standards_kb": triz_engine.format_standards_for_prompt(standards),
            "contradiction": contradiction_text,
            "engineering_desc": c.engineering_desc,
            "constraints": constraints,
        })

        solutions = []
        for item in (result if isinstance(result, list) else [result]):
            solutions.append(SuFieldSolution(
                project_id=c.project_id,
                contradiction_id=c.id,
                standard_code=item.get("standard_code", ""),
                standard_name=item.get("standard_name", ""),
                sufield_model=item.get("sufield_model", ""),
                engineering_mappings=item.get("engineering_mappings", []),
                cost_description=item.get("cost_description", ""),
                experiment_desc=item.get("experiment_desc", ""),
            ))
        return solutions


# Singleton
triz_solve_service = TrizSolveService()
