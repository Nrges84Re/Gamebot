```renpy
# ============================================================
# GameProjectRenPy
# script.rpy
# نسخه متصل به Python Engine + RenPy Bridge
# ============================================================


# ============================================================
# BACKGROUND
# ============================================================

image bg command_center = im.Scale(
    "images/backgrounds/bg_command_center.png",
    config.screen_width,
    config.screen_height
)


# ============================================================
# GAME VARIABLES
# ============================================================

default security = 50
default public_trust = 50
default enemy_influence = 50
default stability = 50
default casualties = 0
default budget = 100
default military = 100
default time_left = 24

default final_score = 50
default result_title = ""
default result_description = ""

default decision_1 = ""
default decision_2 = ""
default decision_3 = ""
default decision_4 = ""


# ============================================================
# PYTHON ENGINE / BRIDGE
# ============================================================

init python:

    # --------------------------------------------------------
    # تلاش برای اتصال به Python Engine
    # --------------------------------------------------------

    try:

        from python_engine.renpy_bridge import RenPyBridge

        crisis_bridge = RenPyBridge()

        python_engine_connected = True

    except Exception:

        crisis_bridge = None

        python_engine_connected = False


    # --------------------------------------------------------
    # همگام‌سازی وضعیت Python با Ren'Py
    # --------------------------------------------------------

    def sync_python_status():

        global security
        global public_trust
        global enemy_influence
        global stability
        global casualties
        global budget
        global military
        global time_left

        if crisis_bridge is None:
            return

        status = crisis_bridge.get_status()

        security = status["security"]
        public_trust = status["public_trust"]
        enemy_influence = status["enemy_influence"]
        stability = status["stability"]
        casualties = status["casualties"]
        budget = status["budget"]
        military = status["military"]
        time_left = status["time_left"]


    # --------------------------------------------------------
    # اجرای تصمیم توسط Python Engine
    # --------------------------------------------------------

    def apply_python_decision(choice_name):

        if crisis_bridge is None:

            renpy.notify(
                "اتصال Python Engine برقرار نیست."
            )

            return False

        try:

            crisis_bridge.apply_decision(choice_name)

            sync_python_status()

            return True

        except Exception as e:

            renpy.notify(
                "خطا در Python Engine: {}".format(e)
            )

            return False


    # --------------------------------------------------------
    # Reset Python Engine
    # --------------------------------------------------------

    def reset_python_engine():

        if crisis_bridge is None:
            return False

        try:

            crisis_bridge.reset()

            sync_python_status()

            return True

        except Exception:

            return False


    # --------------------------------------------------------
    # دریافت نتیجه نهایی
    # --------------------------------------------------------

    def get_python_result():

        global final_score
        global result_title
        global result_description

        if crisis_bridge is None:
            return False

        result = crisis_bridge.get_result()

        final_score = result["score"]
        result_title = result["title"]
        result_description = result["description"]

        return True


    # --------------------------------------------------------
    # محدود کردن مقادیر
    # --------------------------------------------------------

    def clamp_game_values():

        global security
        global public_trust
        global enemy_influence
        global stability
        global casualties
        global budget
        global military
        global time_left

        security = max(0, min(100, security))
        public_trust = max(0, min(100, public_trust))
        enemy_influence = max(0, min(100, enemy_influence))
        stability = max(0, min(100, stability))

        casualties = max(0, casualties)

        budget = max(0, min(100, budget))
        military = max(0, min(100, military))

        time_left = max(0, time_left)


# ============================================================
# CRISIS ENDING SCREEN
# ============================================================

screen crisis_ending():

    modal True

    add Solid("#000000B8")

    frame:
        xalign 0.5
        yalign 0.5

        xsize 1100
        ysize 700

        background Solid("#061522F5")

        padding (40, 30)

        vbox:

            spacing 12

            text "گزارش نهایی عملیات":
                xalign 0.5
                color "#55D6FF"
                size 38
                bold True
                text_align 0.5

            text "مرکز مدیریت بحران":
                xalign 0.5
                color "#B8D4E5"
                size 21
                text_align 0.5

            null height 8

            frame:

                xalign 0.5
                xsize 400

                background Solid("#0A2435EE")

                padding (20, 15)

                vbox:

                    spacing 5

                    text "امتیاز نهایی":
                        xalign 0.5
                        color "#FFFFFF"
                        size 22

                    text "[final_score] / 100":
                        xalign 0.5
                        color "#FFD34D"
                        size 42
                        bold True

            null height 8

            text "[result_title]":
                xalign 0.5
                color "#35E07A"
                size 30
                bold True
                text_align 0.5

            text "[result_description]":
                xalign 0.5
                color "#FFFFFF"
                size 20
                text_align 0.5

            null height 8

            frame:

                xfill True

                background Solid("#081D2BEA")

                padding (20, 15)

                hbox:

                    xfill True
                    spacing 40

                    vbox:

                        xsize 480
                        spacing 8

                        text "امنیت ملی: [security]":
                            color "#FFFFFF"
                            size 19

                        text "اعتماد عمومی: [public_trust]":
                            color "#FFFFFF"
                            size 19

                        text "نفوذ دشمن: [enemy_influence]":
                            color "#FFFFFF"
                            size 19

                        text "ثبات کشور: [stability]":
                            color "#FFFFFF"
                            size 19

                    vbox:

                        xsize 480
                        spacing 8

                        text "تلفات: [casualties]":
                            color "#FF5C5C"
                            size 19

                        text "بودجه: [budget]":
                            color "#35E07A"
                            size 19

                        text "توان نظامی: [military]":
                            color "#35E07A"
                            size 19

                        text "زمان باقی‌مانده: [time_left]":
                            color "#FFD34D"
                            size 19

            null height 10

            hbox:

                xalign 0.5
                spacing 40

                textbutton "ادامه":

                    action Return("continue")

                    text_size 22
                    text_color "#FFFFFF"
                    text_hover_color "#55D6FF"

                textbutton "خروج":

                    action Return("quit")

                    text_size 22
                    text_color "#FFFFFF"
                    text_hover_color "#FF5C5C"


# ============================================================
# START
# ============================================================

label start:

    scene bg command_center

    # --------------------------------------------------------
    # RESET GAME
    # --------------------------------------------------------

    $ reset_python_engine()

    $ security = 50
    $ public_trust = 50
    $ enemy_influence = 50
    $ stability = 50
    $ casualties = 0
    $ budget = 100
    $ military = 100
    $ time_left = 24

    $ final_score = 50

    $ result_title = ""
    $ result_description = ""

    $ decision_1 = ""
    $ decision_2 = ""
    $ decision_3 = ""
    $ decision_4 = ""


    # --------------------------------------------------------
    # INTRO
    # --------------------------------------------------------

    "مرکز مدیریت بحران"

    "سامانه‌های رصدی گزارش می‌دهند که احتمال یک حمله ترکیبی در حال افزایش است."

    "شما مسئول نهایی تصمیم‌گیری هستید."

    "هر تصمیم شما روی امنیت، اعتماد عمومی، نفوذ دشمن، ثبات کشور، بودجه، توان نظامی و تلفات اثر می‌گذارد."


    # ========================================================
    # FIRST DECISION
    # ========================================================

    menu:

        "اعلام آماده‌باش کامل":

            $ decision_1 = "اعلام آماده‌باش کامل"

            $ apply_python_decision("choice_1")

            scene bg command_center

            "دستور اعلام آماده‌باش کامل صادر شد."

            "تمام واحدهای امنیتی در وضعیت آماده‌باش قرار گرفتند."

            "سطح امنیت افزایش یافت، اما اعتماد عمومی کاهش پیدا کرد."

            jump cyber_attack


        "جمع‌آوری اطلاعات بیشتر":

            $ decision_1 = "جمع‌آوری اطلاعات بیشتر"

            $ apply_python_decision("choice_2")

            scene bg command_center

            "دستور جمع‌آوری اطلاعات بیشتر صادر شد."

            "تیم‌های اطلاعاتی شروع به بررسی گزارش‌ها کردند."

            "اطلاعات دقیق‌تری به مرکز بحران ارسال شد."

            jump cyber_attack


        "نادیده گرفتن گزارش":

            $ decision_1 = "نادیده گرفتن گزارش"

            $ apply_python_decision("choice_3")

            scene bg command_center

            "گزارش اولیه نادیده گرفته شد."

            "چند دقیقه بعد، گزارش‌های جدیدی از فعالیت مشکوک دریافت شد."

            jump cyber_attack


# ============================================================
# CYBER ATTACK
# ============================================================

label cyber_attack:

    scene bg command_center

    "⚠ هشدار سایبری"

    "بخشی از زیرساخت دیجیتال کشور در معرض نفوذ قرار گرفته است."

    "تیم فنی درخواست تصمیم فوری دارد."


    menu:

        "فعال‌سازی دفاع سایبری":

            $ decision_2 = "فعال‌سازی دفاع سایبری"

            $ apply_python_decision("choice_4")

            scene bg command_center

            "دفاع سایبری فعال شد."

            "تیم‌های فنی تلاش می‌کنند مسیر نفوذ را مسدود کنند."

            "بخش مهمی از حمله سایبری مهار شد."

            jump crisis_meeting


        "کنترل مرزها":

            $ decision_2 = "کنترل مرزها"

            $ apply_python_decision("choice_5")

            scene bg command_center

            "کنترل مرزها افزایش یافت."

            "نیروهای امنیتی در نقاط حساس مستقر شدند."

            "ورود و خروج در مناطق حساس تحت کنترل قرار گرفت."

            jump crisis_meeting


        "بازداشت افراد مشکوک":

            $ decision_2 = "بازداشت افراد مشکوک"

            $ apply_python_decision("choice_6")

            scene bg command_center

            "افراد مشکوک تحت نظر قرار گرفتند."

            "این تصمیم باعث افزایش امنیت شد، اما نگرانی‌هایی در میان مردم ایجاد کرد."

            jump crisis_meeting


# ============================================================
# CRISIS MEETING
# ============================================================

label crisis_meeting:

    scene bg command_center

    "جلسه ستاد بحران"

    "فرماندهان و مسئولان ارشد بر سر نحوه پاسخ اختلاف نظر دارند."

    "شما باید تصمیم نهایی این مرحله را بگیرید."


    menu:

        "تشکیل کمیته مشترک":

            $ decision_3 = "تشکیل کمیته مشترک"

            $ apply_python_decision("choice_7")

            scene bg command_center

            "کمیته مشترک تشکیل شد."

            "نهادهای مختلف برای هماهنگی پاسخ به بحران همکاری کردند."

            jump final_attack


        "اختیار کامل به نیروهای نظامی":

            $ decision_3 = "اختیار کامل به نیروهای نظامی"

            $ apply_python_decision("choice_8")

            scene bg command_center

            "اختیار کامل عملیات به نیروهای نظامی واگذار شد."

            "سرعت واکنش افزایش یافت."

            "با این حال، فشار بر منابع نظامی و اعتماد عمومی بیشتر شد."

            jump final_attack


        "حمله پیشگیرانه محدود":

            $ decision_3 = "حمله پیشگیرانه محدود"

            $ apply_python_decision("choice_9")

            scene bg command_center

            "حمله پیشگیرانه محدود انجام شد."

            "بخشی از توان عملیاتی دشمن از بین رفت."

            "اما این عملیات هزینه انسانی و نظامی به همراه داشت."

            jump final_attack


# ============================================================
# FINAL ATTACK
# ============================================================

label final_attack:

    scene bg command_center

    "⚠️ حمله نهایی"

    "دشمن فاز اصلی عملیات را آغاز کرده است."

    "اکنون زمان تصمیم تعیین‌کننده فرا رسیده است."


    menu:

        "پاسخ تهاجمی همه‌جانبه":

            $ decision_4 = "پاسخ تهاجمی همه‌جانبه"

            $ apply_python_decision("choice_10")

            scene bg command_center

            "پاسخ تهاجمی همه‌جانبه آغاز شد."

            "نیروهای عملیاتی ضربه سنگینی به زیرساخت‌های دشمن وارد کردند."

            "تهدید اصلی کاهش یافت، اما هزینه عملیات بسیار بالا بود."

            jump calculate_ending


        "دفاع لایه‌ای و کنترل بحران":

            $ decision_4 = "دفاع لایه‌ای و کنترل بحران"

            $ apply_python_decision("choice_11")

            scene bg command_center

            "دفاع لایه‌ای فعال شد."

            "سامانه‌های دفاعی به صورت هماهنگ عمل کردند."

            "بحران با هزینه انسانی کمتر کنترل شد."

            jump calculate_ending


        "فریب اطلاعاتی":

            $ decision_4 = "فریب اطلاعاتی"

            $ apply_python_decision("choice_12")

            scene bg command_center

            "عملیات فریب اطلاعاتی آغاز شد."

            "اطلاعات گمراه‌کننده به شبکه تصمیم‌گیری دشمن منتقل شد."

            "بخشی از عملیات دشمن بدون درگیری مستقیم خنثی شد."

            jump calculate_ending


# ============================================================
# CALCULATE FINAL SCORE
# ============================================================

label calculate_ending:

    scene bg command_center

    # دریافت نتیجه واقعی از Python Engine

    $ sync_python_status()

    $ get_python_result()

    "🏁 مرحله نهایی عملیات به پایان رسید."

    "تمام شاخص‌های بحران توسط Python Engine محاسبه شدند."


    # --------------------------------------------------------
    # نمایش صفحه پایان
    # --------------------------------------------------------

    $ ending_result = renpy.call_screen("crisis_ending")


    if ending_result == "quit":

        return

    else:

        jump start
```
