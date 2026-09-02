# ============================================================
# GameProjectRenPy
# screens.rpy
# نسخه پایدار و اصلاح شده برای Ren'Py 8.3.5
# ============================================================


# ============================================================
# رنگ‌های پروژه
# ============================================================

define crisis_panel_bg = "#061522E8"
define crisis_panel_bg_dark = "#04101AEF"
define crisis_panel_hover = "#102B3EE8"
define crisis_panel_selected = "#17445FE8"

define crisis_text_main = "#FFFFFF"
define crisis_text_secondary = "#B8D4E5"
define crisis_text_blue = "#55D6FF"
define crisis_text_green = "#35E07A"
define crisis_text_yellow = "#FFD34D"
define crisis_text_red = "#FF5C5C"


# ============================================================
# SAY SCREEN
# پیام‌های داستان
# ============================================================

screen say(who, what):

    window:
        id "window"

        style "say_window"

        xalign 0.5
        yalign 0.86

        xmaximum 1250
        ymaximum 230

        background Solid("#061522E8")

        padding (35, 25)

        if who:

            text who:
                id "who"

                style "say_label"

                xalign 0.5
                text_align 0.5

        text what:
            id "what"

            style "say_dialogue"

            xalign 0.5
            text_align 0.5


# ============================================================
# SAY STYLES
# ============================================================

style say_window:

    background Solid("#061522E8")

    padding (35, 25)


style say_label:

    color "#55D6FF"

    size 30

    bold True

    xalign 0.5

    text_align 0.5


style say_dialogue:

    color "#FFFFFF"

    size 30

    xalign 0.5

    text_align 0.5


# ============================================================
# CHOICE SCREEN
# انتخاب تصمیم
# ============================================================

screen choice(items):

    modal True

    use crisis_status


    frame:

        xalign 0.50
        yalign 0.78

        xsize 900

        background Solid("#061522ED")

        padding (28, 28)


        vbox:

            spacing 14


            text "🎯  تصمیم خود را انتخاب کنید":

                xalign 0.5

                color "#FFFFFF"

                size 30

                bold True

                text_align 0.5


            for i in items:

                button:

                    xfill True

                    xminimum 700

                    yminimum 70

                    background Solid("#0A1E2DEB")

                    hover_background Solid("#17445FEF")

                    action i.action

                    padding (20, 12)


                    text i.caption:

                        xalign 0.5

                        yalign 0.5

                        color "#FFFFFF"

                        hover_color "#55D6FF"

                        size 24

                        text_align 0.5


# ============================================================
# پنل وضعیت بحران
# گوشه بالا سمت راست
# ============================================================

screen crisis_status():

    frame:

        xalign 0.965
        yalign 0.035

        xsize 350

        background Solid("#061522EE")

        padding (22, 20)


        vbox:

            spacing 9


            # ------------------------------------------------
            # عنوان
            # ------------------------------------------------

            text "📊  وضعیت بحران":

                xalign 0.5

                color "#55D6FF"

                size 28

                bold True

                text_align 0.5


            null height 2


            # ------------------------------------------------
            # امنیت ملی
            # ------------------------------------------------

            text "امنیت ملی: [security]":

                color "#FFFFFF"

                size 19


            bar:

                value security

                range 100

                xmaximum 305

                ymaximum 16

                left_bar Solid("#35E07A")

                right_bar Solid("#122534")


            # ------------------------------------------------
            # اعتماد عمومی
            # ------------------------------------------------

            text "اعتماد عمومی: [public_trust]":

                color "#FFFFFF"

                size 19


            bar:

                value public_trust

                range 100

                xmaximum 305

                ymaximum 16

                left_bar Solid("#FFD34D")

                right_bar Solid("#122534")


            # ------------------------------------------------
            # نفوذ دشمن
            # ------------------------------------------------

            text "نفوذ دشمن: [enemy_influence]":

                color "#FFFFFF"

                size 19


            bar:

                value enemy_influence

                range 100

                xmaximum 305

                ymaximum 16

                left_bar Solid("#FF5C5C")

                right_bar Solid("#122534")


            # ------------------------------------------------
            # ثبات کشور
            # ------------------------------------------------

            text "ثبات کشور: [stability]":

                color "#FFFFFF"

                size 19


            bar:

                value stability

                range 100

                xmaximum 305

                ymaximum 16

                left_bar Solid("#35E07A")

                right_bar Solid("#122534")


            null height 4


            # ------------------------------------------------
            # اطلاعات عددی
            # ------------------------------------------------

            hbox:

                xfill True


                text "تلفات":

                    color "#FFFFFF"

                    size 18


                null width 10


                text "[casualties]":

                    xalign 1.0

                    color "#FF5C5C"

                    size 18


            hbox:

                xfill True


                text "بودجه":

                    color "#FFFFFF"

                    size 18


                null width 10


                text "[budget]":

                    xalign 1.0

                    color "#FFD34D"

                    size 18


            hbox:

                xfill True


                text "توان نظامی":

                    color "#FFFFFF"

                    size 18


                null width 10


                text "[military]":

                    xalign 1.0

                    color "#35E07A"

                    size 18


            hbox:

                xfill True


                text "زمان باقی‌مانده":

                    color "#FFFFFF"

                    size 18


                null width 10


                text "[time_left] دقیقه":

                    xalign 1.0

                    color "#FFD34D"

                    size 18


# ============================================================
# NOTIFICATION PANEL
# ============================================================

screen game_notification(title="هشدار", message="", level="normal"):

    frame:

        xalign 0.82

        yalign 0.38

        xsize 450

        background Solid("#061522EE")

        padding (22, 20)


        vbox:

            spacing 8


            text "[title]":

                color "#55D6FF"

                size 24

                bold True


            text "[message]":

                color "#FFFFFF"

                size 19

                text_align 0.0


# ============================================================
# DECISION REPORT
# ============================================================

screen decision_report(title="گزارش تصمیم", message=""):

    modal True


    frame:

        xalign 0.5

        yalign 0.5

        xsize 650

        background Solid("#061522F2")

        padding (35, 30)


        vbox:

            spacing 15


            text "📊 [title]":

                xalign 0.5

                color "#55D6FF"

                size 30

                bold True

                text_align 0.5


            text "[message]":

                xalign 0.5

                color "#FFFFFF"

                size 22

                text_align 0.5


            textbutton "ادامه":

                xalign 0.5

                action Hide("decision_report")

                text_size 22

                text_color "#FFFFFF"

                text_hover_color "#55D6FF"


# ============================================================
# ENDING PANEL
# صفحه پایان
# ============================================================

screen ending_panel():

    modal True


    add Solid("#00000099")


    frame:

        xalign 0.5

        yalign 0.5

        xsize 1050

        ysize 720

        background Solid("#061522F5")

        padding (45, 35)


        vbox:

            spacing 14


            text "🏁  گزارش نهایی عملیات":

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


            null height 5


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


            null height 5


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


            null height 5


            frame:

                xfill True

                background Solid("#081D2BEA")

                padding (20, 15)


                hbox:

                    xfill True

                    spacing 40


                    vbox:

                        xsize 430

                        spacing 8


                        text "🔐 امنیت ملی: [security]":

                            color "#FFFFFF"

                            size 19


                        text "👥 اعتماد عمومی: [public_trust]":

                            color "#FFFFFF"

                            size 19


                        text "☠️ نفوذ دشمن: [enemy_influence]":

                            color "#FFFFFF"

                            size 19


                        text "🏛️ ثبات کشور: [stability]":

                            color "#FFFFFF"

                            size 19


                    vbox:

                        xsize 430

                        spacing 8


                        text "💀 تلفات: [casualties]":

                            color "#FFFFFF"

                            size 19


                        text "💰 بودجه: [budget]":

                            color "#FFFFFF"

                            size 19


                        text "⚔️ توان نظامی: [military]":

                            color "#FFFFFF"

                            size 19


                        text "⏱️ زمان باقی‌مانده: [time_left]":

                            color "#FFFFFF"

                            size 19


            null height 10


            hbox:

                xalign 0.5

                spacing 25


                textbutton "🔄 شروع بازی جدید":

                    action [Hide("ending_panel"), Start()]

                    text_size 21

                    text_color "#FFFFFF"

                    text_hover_color "#55D6FF"


                textbutton "🚪 خروج":

                    action Quit(confirm=True)

                    text_size 21

                    text_color "#FFFFFF"

                    text_hover_color "#FF5C5C"


# ============================================================
# QUICK MENU
# عمداً خالی است
# ============================================================

screen quick_menu():

    pass


# ============================================================
# GAME OVERLAY
# ============================================================

screen game_overlay():

    use crisis_status


# ============================================================
# MAIN MENU
# ============================================================

screen main_menu():

    tag menu


    add "bg command_center"


    frame:

        xalign 0.5

        yalign 0.5

        xsize 700

        background Solid("#061522ED")

        padding (40, 35)


        vbox:

            spacing 20


            text "مرکز مدیریت بحران":

                xalign 0.5

                color "#55D6FF"

                size 38

                bold True

                text_align 0.5


            text "سامانه شبیه‌سازی تصمیم‌گیری بحران":

                xalign 0.5

                color "#B8D4E5"

                size 20

                text_align 0.5


            null height 20


            textbutton "🎯 شروع بازی":

                xalign 0.5

                action Start()

                text_size 25

                text_color "#FFFFFF"

                text_hover_color "#55D6FF"


            textbutton "🚪 خروج":

                xalign 0.5

                action Quit(confirm=True)

                text_size 25

                text_color "#FFFFFF"

                text_hover_color "#FF5C5C"


# ============================================================
# CONFIRM SCREEN
# ============================================================

screen confirm(message, yes_action, no_action):

    modal True


    frame:

        xalign 0.5

        yalign 0.5

        xsize 650

        background Solid("#061522F5")

        padding (35, 30)


        vbox:

            spacing 20


            text "[message]":

                xalign 0.5

                color "#FFFFFF"

                size 24

                text_align 0.5


            hbox:

                xalign 0.5

                spacing 35


                textbutton "بله":

                    action yes_action

                    text_size 21

                    text_color "#FFFFFF"

                    text_hover_color "#35E07A"


                textbutton "خیر":

                    action no_action

                    text_size 21

                    text_color "#FFFFFF"

                    text_hover_color "#FF5C5C"