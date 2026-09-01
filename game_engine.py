from engine.story_manager import story_manager
from engine.choice_manager import choice_manager
from engine.event_manager import event_manager
from engine.condition_manager import condition_manager
from engine.ending_manager import ending_manager
from engine.resource_manager import resource_manager
from engine.time_manager import time_manager
from engine.save_manager import save_manager


class GameEngine:

    # =========================================
    # شروع بازی
    # =========================================

    def start(self, user_id: int):
        data = save_manager.load_or_create(user_id)

        # اگر بازی قبلاً تمام شده باشد
        if data["is_over"]:
            return self._build_game_over_response(
                data["state"]
            )

        return self._build_scene_response(
            data["current_scene"],
            data["state"],
            data["is_over"]
        )

    # =========================================
    # شروع مجدد بازی
    # =========================================

    def restart(self, user_id: int):
        data = save_manager.reset(user_id)

        return self._build_scene_response(
            data["current_scene"],
            data["state"],
            False
        )

    # =========================================
    # انتخاب کاربر
    # =========================================

    def choose(self, user_id: int, index: int):

        data = save_manager.load_or_create(user_id)

        # -----------------------------------------
        # اگر بازی قبلاً تمام شده
        # -----------------------------------------

        if data["is_over"]:
            return self._build_game_over_response(
                data["state"]
            )

        current_scene_id = data["current_scene"]
        state = data["state"]

        # -----------------------------------------
        # دریافت صحنه
        # -----------------------------------------

        scene = story_manager.get_scene(current_scene_id)

        if not scene:
            return {
                "type": "error",
                "text": f"صحنه '{current_scene_id}' پیدا نشد.",
                "buttons": []
            }

        choices = scene.get("choices", [])

        # -----------------------------------------
        # بررسی شماره انتخاب
        # -----------------------------------------

        if index < 1 or index > len(choices):

            buttons = []

            for cid in choices:

                choice = choice_manager.get_choice(cid)

                if choice:
                    buttons.append(
                        choice.get("text", "گزینه بدون متن")
                    )

            return {
                "type": "error",
                "text": "شماره انتخاب نامعتبر است.",
                "buttons": buttons
            }

        # -----------------------------------------
        # دریافت انتخاب
        # -----------------------------------------

        choice_id = choices[index - 1]

        choice = choice_manager.get_choice(choice_id)

        if not choice:
            return {
                "type": "error",
                "text": f"انتخاب '{choice_id}' پیدا نشد.",
                "buttons": []
            }

        # -----------------------------------------
        # اعمال Event
        # -----------------------------------------

        event_id = choice.get("event")
        next_scene = choice.get("next_scene")

        event_manager.apply(
            state,
            event_id
        )

        # -----------------------------------------
        # کاهش زمان
        # -----------------------------------------

        time_manager.decrease_time(
            state,
            1
        )

        # -----------------------------------------
        # پایان به دلیل تمام شدن زمان
        # -----------------------------------------

        if state.get("time", 0) <= 0:

            return self._finish_game(
                user_id,
                state,
                "time"
            )

        # -----------------------------------------
        # بررسی شرایط پایان
        # -----------------------------------------

        ending_id = condition_manager.check(state)

        if ending_id:

            ending = ending_manager.get_ending(
                ending_id
            )

            if ending:

                return self._finish_game(
                    user_id,
                    state,
                    "condition",
                    ending
                )

        # -----------------------------------------
        # اگر صحنه بعدی وجود ندارد
        # -----------------------------------------

        if not next_scene:

            return self._finish_game(
                user_id,
                state,
                "scenario"
            )

        # -----------------------------------------
        # ذخیره بازی
        # -----------------------------------------

        save_manager.save(
            user_id,
            next_scene,
            state,
            False
        )

        # -----------------------------------------
        # اگر رسیدیم به صحنه نهایی
        # -----------------------------------------

        if next_scene == "scene_010":

            return self._finish_game(
                user_id,
                state,
                "final_scene"
            )

        # -----------------------------------------
        # نمایش صحنه بعد
        # -----------------------------------------

        return self._build_scene_response(
            next_scene,
            state,
            False
        )

    # =========================================
    # پایان بازی
    # =========================================

    def _finish_game(
        self,
        user_id: int,
        state: dict,
        reason: str,
        ending=None
    ):

        score = self._calculate_score(state)

        result = self._get_result(score)

        if ending:

            title = ending.get(
                "title",
                result["title"]
            )

            ending_text = ending.get(
                "text",
                ""
            )

        elif reason == "time":

            title = "⏰ زمان به پایان رسید"

            ending_text = (
                "زمان تصمیم‌گیری شما به پایان رسید "
                "و بحران از کنترل خارج شد."
            )

        else:

            title = result["title"]

            ending_text = result["text"]

        # -----------------------------------------
        # متن نهایی
        # -----------------------------------------

        final_text = (
            "🏁 پایان بازی\n\n"
            f"🎯 {title}\n\n"
            f"{ending_text}\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "📊 ارزیابی نهایی\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            f"🛡 امنیت: {state.get('security', 0)}\n"
            f"👥 اعتماد عمومی: {state.get('public_trust', 0)}\n"
            f"☠️ نفوذ دشمن: {state.get('enemy_influence', 0)}\n"
            f"⚖️ ثبات: {state.get('stability', 0)}\n"
            f"💀 تلفات: {state.get('casualties', 0)}\n"
            f"💰 بودجه: {state.get('budget', 0)}\n"
            f"⚔️ توان نظامی: {state.get('military', 0)}\n"
            f"⏱ زمان باقی‌مانده: {state.get('time', 0)}\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"🏆 امتیاز نهایی: {score} / 100\n"
            f"📌 نتیجه: {result['level']}\n"
            "━━━━━━━━━━━━━━━━━━"
        )

        # -----------------------------------------
        # ذخیره به عنوان بازی تمام‌شده
        # -----------------------------------------

        save_manager.save(
            user_id,
            "scene_010",
            state,
            True
        )

        return {
            "type": "game_over",
            "text": final_text,
            "buttons": [],
            "is_over": True,
            "score": score,
            "result": result["level"],
            "state": state
        }

    # =========================================
    # محاسبه امتیاز
    # =========================================

    def _calculate_score(self, state: dict):

        security = state.get("security", 0)
        public_trust = state.get("public_trust", 0)
        enemy_influence = state.get("enemy_influence", 0)
        stability = state.get("stability", 0)
        casualties = state.get("casualties", 0)
        budget = state.get("budget", 0)

        # -----------------------------------------
        # امتیاز پایه
        # -----------------------------------------

        score = 0

        score += security * 0.25
        score += public_trust * 0.20
        score += stability * 0.25

        # کاهش نفوذ دشمن امتیاز مثبت دارد
        score += (100 - enemy_influence) * 0.15

        # بودجه
        score += budget * 0.10

        # تلفات
        casualty_penalty = min(
            casualties * 2,
            20
        )

        score -= casualty_penalty

        # محدود کردن بین 0 و 100
        score = max(
            0,
            min(
                100,
                round(score)
            )
        )

        return score

    # =========================================
    # تعیین نتیجه
    # =========================================

    def _get_result(self, score):

        if score >= 85:

            return {
                "level": "🏆 پیروزی عالی",
                "title": "مدیریت بحران فوق‌العاده",
                "text": (
                    "شما توانستید بحران را با کمترین "
                    "هزینه و بیشترین ثبات مدیریت کنید."
                )
            }

        elif score >= 70:

            return {
                "level": "🥇 موفقیت",
                "title": "مدیریت موفق بحران",
                "text": (
                    "تصمیم‌های شما باعث شد کشور از "
                    "بحران عبور کند و شرایط تحت کنترل باقی بماند."
                )
            }

        elif score >= 50:

            return {
                "level": "🥈 موفقیت نسبی",
                "title": "بحران با هزینه بالا کنترل شد",
                "text": (
                    "بحران کنترل شد، اما برخی تصمیم‌ها "
                    "هزینه‌های قابل توجهی برای کشور داشتند."
                )
            }

        else:

            return {
                "level": "❌ شکست",
                "title": "بحران از کنترل خارج شد",
                "text": (
                    "تصمیم‌های اتخاذشده نتوانستند "
                    "بحران را به شکل مطلوب کنترل کنند."
                )
            }

    # =========================================
    # پاسخ بازی تمام شده
    # =========================================

    def _build_game_over_response(self, state):

        score = self._calculate_score(state)

        result = self._get_result(score)

        text = (
            "🏁 بازی قبلی تمام شده است.\n\n"
            f"🏆 امتیاز نهایی: {score} / 100\n"
            f"📌 نتیجه: {result['level']}\n\n"
            "برای شروع یک بازی جدید، /restart را بزنید."
        )

        return {
            "type": "game_over",
            "text": text,
            "buttons": [],
            "is_over": True,
            "score": score,
            "result": result["level"],
            "state": state
        }

    # =========================================
    # ساخت پاسخ صحنه
    # =========================================

    def _build_scene_response(
        self,
        scene_id: str,
        state: dict,
        is_over: bool
    ):

        scene = story_manager.get_scene(
            scene_id
        )

        if not scene:

            return {
                "type": "error",
                "text": f"صحنه '{scene_id}' پیدا نشد.",
                "buttons": []
            }

        status_text = self._format_status(
            state
        )

        scene_text = (
            f"🎯 {scene.get('title', 'بدون عنوان')}\n\n"
            f"{scene.get('text', '')}"
        )

        buttons = []

        for choice_id in scene.get(
            "choices",
            []
        ):

            choice = choice_manager.get_choice(
                choice_id
            )

            if choice:

                buttons.append(
                    choice.get(
                        "text",
                        "گزینه بدون متن"
                    )
                )

        return {
            "type": "scene",
            "scene_id": scene_id,
            "text": (
                f"{status_text}\n\n"
                f"{scene_text}"
            ),
            "buttons": buttons,
            "is_over": is_over,
            "state": state
        }

    # =========================================
    # نمایش وضعیت
    # =========================================

    def _format_status(self, state: dict):

        resources = resource_manager.get_resources(
            state
        )

        return (
            "📊 وضعیت بحران\n"
            f"امنیت: {state.get('security', 0)}\n"
            f"اعتماد عمومی: {state.get('public_trust', 0)}\n"
            f"نفوذ دشمن: {state.get('enemy_influence', 0)}\n"
            f"ثبات: {state.get('stability', 0)}\n"
            f"تلفات: {state.get('casualties', 0)}\n"
            f"بودجه: {resources.get('budget', 0)}\n"
            f"توان نظامی: {resources.get('military', 0)}\n"
            f"زمان: {resources.get('time', 0)}"
        )


game_engine = GameEngine()
