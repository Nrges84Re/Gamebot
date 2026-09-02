# ============================================================
# GameProjectRenPy
# python_bridge.rpy
# اتصال Ren'Py به Python Engine
# همراه با هماهنگ‌سازی Save / Load
# ============================================================


# ============================================================
# PYTHON SAVE STATE
# ============================================================

default python_saved_state = None


# ============================================================
# PYTHON BRIDGE
# ============================================================

init python:

    import sys
    import os


    # --------------------------------------------------------
    # مسیر Python Engine
    # --------------------------------------------------------

    PYTHON_ENGINE_PATH = os.path.join(
        config.basedir,
        "python_engine"
    )


    if PYTHON_ENGINE_PATH not in sys.path:
        sys.path.append(PYTHON_ENGINE_PATH)


    # --------------------------------------------------------
    # اتصال به Python Engine
    # --------------------------------------------------------

    try:

        from renpy_bridge import RenPyBridge

        python_bridge = RenPyBridge()

        python_bridge_status = "اتصال Python موفق است."


    except Exception as e:

        python_bridge = None

        python_bridge_status = (
            "خطا در اتصال Python: " + str(e)
        )


    # ========================================================
    # RESET PYTHON ENGINE
    # ========================================================

    def reset_python_engine():

        if python_bridge is None:
            return

        python_bridge.reset()


    # ========================================================
    # APPLY DECISION
    # ========================================================

    def apply_python_decision(decision):

        if python_bridge is None:
            return None

        return python_bridge.apply_decision(decision)


    # ========================================================
    # SYNC PYTHON → REN'PY
    # ========================================================

    def sync_python_status():

        global security
        global public_trust
        global enemy_influence
        global stability
        global casualties
        global budget
        global military
        global time_left


        if python_bridge is None:
            return


        status = python_bridge.get_status()


        security = status["security"]
        public_trust = status["public_trust"]
        enemy_influence = status["enemy_influence"]
        stability = status["stability"]
        casualties = status["casualties"]
        budget = status["budget"]
        military = status["military"]
        time_left = status["time_left"]


    # ========================================================
    # GET FINAL RESULT
    # ========================================================

    def get_python_result():

        global final_score
        global result_title
        global result_description


        if python_bridge is None:
            return None


        result = python_bridge.get_result()


        final_score = result["score"]
        result_title = result["title"]
        result_description = result["description"]


        return result


    # ========================================================
    # GET PYTHON STATE
    # ========================================================

    def get_python_save_state():

        if python_bridge is None:
            return None

        return python_bridge.get_state().copy()


    # ========================================================
    # LOAD PYTHON STATE
    # ========================================================

    def load_python_save_state(state):

        if python_bridge is None:
            return

        if state is None:
            return

        python_bridge.load_state(state)

        sync_python_status()


    # ========================================================
    # PREPARE PYTHON STATE BEFORE SAVE
    # ========================================================

    def prepare_python_for_save():

        global python_saved_state


        if python_bridge is None:
            return


        python_saved_state = python_bridge.get_state().copy()


    # ========================================================
    # RESTORE PYTHON STATE AFTER LOAD
    # ========================================================

    def restore_python_after_load():

        global python_saved_state


        if python_bridge is None:
            return


        if python_saved_state is None:
            return


        python_bridge.load_state(
            python_saved_state
        )


        sync_python_status()
    # ========================================================
    # REN'PY LOAD CALLBACK
    # ========================================================

    config.after_load_callbacks.append(
        restore_python_after_load
    )


   