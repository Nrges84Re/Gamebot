import json
from config import INITIAL_SCENE_ID
from database.database import get_player, upsert_player, reset_player
from engine.variable_manager import variable_manager


class SaveManager:
    def load(self, user_id: int):
        row = get_player(user_id)
        if not row:
            return None

        _, current_scene, state_json, is_over = row
        return {
            "user_id": user_id,
            "current_scene": current_scene,
            "state": json.loads(state_json),
            "is_over": bool(is_over)
        }

    def create_new(self, user_id: int):
        state = variable_manager.new_state()
        data = {
            "user_id": user_id,
            "current_scene": INITIAL_SCENE_ID,
            "state": state,
            "is_over": False
        }
        upsert_player(
            user_id=user_id,
            current_scene=data["current_scene"],
            state_json=json.dumps(data["state"], ensure_ascii=False),
            is_over=0
        )
        return data

    def load_or_create(self, user_id: int):
        data = self.load(user_id)
        if data is None:
            data = self.create_new(user_id)
        return data

    def save(self, user_id: int, current_scene: str, state: dict, is_over: bool):
        upsert_player(
            user_id=user_id,
            current_scene=current_scene,
            state_json=json.dumps(state, ensure_ascii=False),
            is_over=1 if is_over else 0
        )

    def reset(self, user_id: int):
        state = variable_manager.new_state()
        reset_player(
            user_id=user_id,
            current_scene=INITIAL_SCENE_ID,
            state_json=json.dumps(state, ensure_ascii=False)
        )
        return {
            "user_id": user_id,
            "current_scene": INITIAL_SCENE_ID,
            "state": state,
            "is_over": False
        }


save_manager = SaveManager()
