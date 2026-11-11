# WCPS core
This is the core package of pywcps. Both the Authentication and GameServer depend on it for basic server-server communication as well as packet handling.

This package is version agnostic: both the Code Name Legacy (PF23) `main` and the
frozen PF20 reference (`pf20` branches of wcps_auth and wcps_game) use its `main`.
