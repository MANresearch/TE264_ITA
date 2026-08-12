import unittest

import numpy as np

import fuzzy_core as fc
from te264_historical_data import gerar_portfolio_calibrado


class FuzzyCoreTests(unittest.TestCase):
    def test_rule_convergence_counts(self):
        result = fc.analise_convergencia()
        self.assertEqual(result["concordancia_total"], 12)
        self.assertEqual(result["concordancia_parcial"], 4)
        self.assertEqual(result["divergencia_total"], 0)
        self.assertEqual(result["total_combinacoes"], 16)

    def test_boundary_outputs_are_finite_and_ordered(self):
        low = fc.inferir_mamdani(0.0, 0.0)
        high = fc.inferir_mamdani(1.0, 1.0)
        self.assertTrue(np.isfinite(low))
        self.assertTrue(np.isfinite(high))
        self.assertGreater(high, low)
        self.assertGreaterEqual(low, 0.0)
        self.assertLessEqual(high, 1.0)

    def test_surface_has_no_material_local_reversals(self):
        _, _, surface = fc.superficie_decisao(n=41)
        self.assertEqual(int(np.isnan(surface).sum()), 0)
        self.assertGreaterEqual(float(np.diff(surface, axis=0).min()), -0.01)
        self.assertGreaterEqual(float(np.diff(surface, axis=1).min()), -0.01)

    def test_synthetic_portfolio_is_reproducible_and_reconciles(self):
        first = gerar_portfolio_calibrado(n=200, cenario="stress", seed=42)
        second = gerar_portfolio_calibrado(n=200, cenario="stress", seed=42)
        self.assertTrue(first.equals(second))
        self.assertEqual(len(first), 200)
        self.assertTrue(first["pd"].between(0.0, 1.0).all())
        self.assertTrue(first["lgd"].between(0.0, 1.0).all())
        expected_loss = first["pd"] * first["lgd"] * first["ead"]
        # EL is calculated before display rounding of PD and LGD.
        self.assertTrue(np.allclose(first["el"], expected_loss, rtol=2e-4, atol=2.0))


if __name__ == "__main__":
    unittest.main()
