from libqtile import bar, layout
from libqtile.widget import base
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from qtile_extras import widget
from libqtile import extension
from qtile_extras.widget.decorations import RectDecoration


class ClickableClock(widget.Clock):
    def __init__(self, **config):
        widget.Clock.__init__(self, **config)
        self.format = config['primary']
        self.primary = config['primary']
        self.secondary = config['secondary']
        self.mouse_callbacks = {
            'Button1': self.switch_format
        }

    def switch_format(self):
        self.format = self.secondary if self.format == self.primary else self.primary
        self.bar.draw()


class KeyboardLanguage(base.ThreadPoolText, base.MarginMixin, base.PaddingMixin):

    def __init__(self, **config):
        base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(base.MarginMixin.defaults)
        self.add_defaults(base.PaddingMixin.defaults)
        self.update_interval = 1

    def poll(self):
        return self.call_process("xkb-switch -p".split())[0:2].upper()


mod = "mod4"
terminal = "alacritty"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "e", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    Key([], "XF86AudioMute", lazy.spawn("amixer set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer set Master 5%- unmute")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer set Master 5%+ unmute")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl s 5%-")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl s +5%")),
    Key([mod], "s", lazy.spawn("flameshot gui")),
    Key([mod], "m", lazy.spawn("xkb-switch -n")),
    Key([mod], "b", lazy.hide_show_bar()),
    Key([mod], "x", lazy.hide_show_bar()),
    Key([mod, "control"], 't', lazy.run_extension(extension.CommandSet(
        commands={
            'shutdown': 'systemctl shutdown',
            'reboot': 'systemctl reboot',
            'lock': 'systemctl suspend',
            'suspend': 'systemctl suspend',
        },
        background="#1e1e2e",
        selected_background="#f38ba8",
        selected_foreground="#1e1e2e",
        foreground="#cdd6f4",
        fontsize=12,
        dmenu_height=30
    ))),
    Key([mod], 'p', lazy.run_extension(extension.DmenuRun(
        dmenu_prompt="Run:",
        background="#1e1e2e",
        selected_background="#f38ba8",
        selected_foreground="#1e1e2e",
        foreground="#cdd6f4",
        fontsize=12,
        # font="Jetbrains Mono SemiBold",
        dmenu_height=30  # Only supported by some dmenu forks
    ))),
]
# 一二三四五六七八九

groups = [
    Group("1", label="一"),
    Group("2", label="二"),
    Group("3", label="三"),
    Group("4", label="四"),
    Group("5", label="五"),
    Group("6", label="六"),
    Group("7", label="七"),
    Group("8", label="八"),
    Group("9", label="九"),
]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(
                    i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )
layout_defaults = {
    "margin": 8,
    "border_width": 2,
    "border_focus": "#74c7ec",
    "border_normal": "#7f849c",
    "border_on_single": True
}

layouts = [
    # layout.MonadTall(**layout_defaults),
    layout.Columns(**layout_defaults),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2, **layout_defaults),
    # layout.Bsp(**layout_defaults),
    # layout.Matrix(**layout_defaults),
    # layout.MonadWide(**layout_defaults),
    layout.RatioTile(**layout_defaults),
    # layout.Tile(**layout_defaults),
    layout.TreeTab(**layout_defaults),
    # layout.VerticalTile(**layout_defaults),
    # layout.Zoomy(**layout_defaults),
]
widget_defaults = dict(
    font="JetBrainsMonoExtraBold Nerd Font",
    fontsize=14,
    padding=3,
)
extension_defaults = widget_defaults.copy()
decor = {
    "decorations": [
        RectDecoration(
            use_widget_background=True,
            radius=2,
            filled=True,
            padding_x=4,
            padding_y=5
        )
    ],
    "padding": 8,
}
screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    font="Ma Shan Zheng",
                    highlight_method='block',
                    this_current_screen_border="#f38ba8",
                    # rounded=Falsee,
                    inactive="#7f849c",
                    foreground="#ffffff",
                    borderwidth=2,
                    padding=4,
                    block_highlight_text_color="#1e1e2e",
                    urgent_alert_method="text",
                    urgent_text="#f38ba8"
                ),
                widget.CurrentLayoutIcon(
                    scale=0.5,
                    background="#89b4fa",
                    decorations=[
                        RectDecoration(
                            use_widget_background=True,
                            radius=2,
                            filled=True,
                            padding_x=4,
                            padding_y=4
                        )
                    ]
                ),
                widget.Prompt(prompt="RUN: ", cursorblink=0,),
                widget.Spacer(),
                # KeyboardLanguage(
                #     background="#74c7ec",
                #     **decor
                # ),
                widget.CheckUpdates(
                    display_format=" {updates}",
                    no_update_string=" No Updates",
                    background="#94e2d5",
                    colour_have_updates="#1e1e2e",
                    colour_no_updates="#1e1e2e",
                    execute="alacritty -e sudo pacman -Syu",
                    **decor
                ),
                widget.Backlight(
                    fmt=" {}",
                    backlight_name="intel_backlight",
                    background="#fab387",
                    foreground="#1e1e2e",
                    **decor
                ),
                widget.Battery(
                    format="{percent:2.0%}{char}",
                    fmt=" {}",
                    charge_char="+",
                    discharge_char="-",
                    full_char="=",
                    background="#a6e3a1",
                    foreground="#1e1e2e",
                    show_short_text=False,
                    **decor
                ),
                widget.Volume(
                    fmt=" {}",
                    background="#cba6f7",
                    foreground="#1e1e2e",
                    **decor
                ),
                ClickableClock(
                    primary=" %I:%M:%S %p",
                    secondary="\uf073 %d-%m-%Y",
                    background="#74c7ec",
                    foreground="#1e1e2e",
                    **decor
                )
            ],
            30,
            background="#1e1e2e",
            # margin=[8, 8, 0, 8],
            # border_width=1,  # Draw top and bottom borders
            # border_color="74c7ec"  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ],
    **layout_defaults
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
