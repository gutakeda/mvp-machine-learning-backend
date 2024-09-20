import numpy as np

class PreProcessador:
    def preparar_form(form):
        """Prepara os dados recebidos do front para serem usados no modelo."""
        X_input = np.array([form["age"],
                            form["sex"],
                            form["chest_pain_type"],
                            form["resting_bp"],
                            form["cholesterol"],
                            form["fasting_bs"],
                            form["resting_ecg"],
                            form["max_hr"],
                            form["exercise_angina"],
                            form["oldpeak"],
                            form["st_slope"],
                        ])
        print(X_input)
        X_input = X_input.reshape(1, -1)
        print(X_input)
        return X_input