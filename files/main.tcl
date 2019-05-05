#############################################################################
# Generated by PAGE version 4.22
#  in conjunction with Tcl version 8.6
#  Apr 16, 2019 12:43:01 AM +0300  platform: Windows NT
set vTcl(timestamp) ""


if {!$vTcl(borrow)} {

set vTcl(actual_gui_bg) #d9d9d9
set vTcl(actual_gui_fg) #000000
set vTcl(actual_gui_analog) #ececec
set vTcl(actual_gui_menu_analog) #ececec
set vTcl(actual_gui_menu_bg) #d9d9d9
set vTcl(actual_gui_menu_fg) #000000
set vTcl(complement_color) #d9d9d9
set vTcl(analog_color_p) #d9d9d9
set vTcl(analog_color_m) #ececec
set vTcl(active_fg) #000000
set vTcl(actual_gui_menu_active_bg)  #ececec
set vTcl(active_menu_fg) #000000
}

#################################
#LIBRARY PROCEDURES
#


if {[info exists vTcl(sourcing)]} {

proc vTcl:project:info {} {
    set base .top42
    global vTcl
    set base $vTcl(btop)
    if {$base == ""} {
        set base .top42
    }
    namespace eval ::widgets::$base {
        set dflt,origin 0
        set runvisible 1
    }
    namespace eval ::widgets_bindings {
        set tagslist _TopLevel
    }
    namespace eval ::vTcl::modules::main {
        set procs {
        }
        set compounds {
        }
        set projectType single
    }
}
}

#################################
# GENERATED GUI PROCEDURES
#

proc vTclWindow.top42 {base} {
    if {$base == ""} {
        set base .top42
    }
    if {[winfo exists $base]} {
        wm deiconify $base; return
    }
    set top $base
    ###################
    # CREATING WIDGETS
    ###################
    vTcl::widgets::core::toplevel::createCmd $top -class Toplevel \
        -background {#d9d9d9} -highlightbackground {#d9d9d9} \
        -highlightcolor black 
    wm focusmodel $top passive
    wm geometry $top 784x536+476+183
    update
    # set in toplevel.wgt.
    global vTcl
    global img_list
    set vTcl(save,dflt,origin) 0
    wm maxsize $top 1924 1061
    wm minsize $top 120 1
    wm overrideredirect $top 0
    wm resizable $top 1 1
    wm deiconify $top
    wm title $top "New Toplevel"
    vTcl:DefineAlias "$top" "top_level" vTcl:Toplevel:WidgetProc "" 1
    ttk::style configure TNotebook -background #d9d9d9
    ttk::style configure TNotebook.Tab -background #d9d9d9
    ttk::style configure TNotebook.Tab -foreground #000000
    ttk::style configure TNotebook.Tab -font "TkDefaultFont"
    ttk::style map TNotebook.Tab -background [list disabled #d9d9d9 selected #d9d9d9]
    ttk::notebook $top.tNo43 \
        -width 784 -height 536 -takefocus {} 
    vTcl:DefineAlias "$top.tNo43" "notebook" vTcl:WidgetProc "top_level" 1
    frame $top.tNo43.t0 \
        -background {#d9d9d9} -highlightbackground {#d9d9d9} \
        -highlightcolor black 
    vTcl:DefineAlias "$top.tNo43.t0" "notebook_t0" vTcl:WidgetProc "top_level" 1
    $top.tNo43 add $top.tNo43.t0 \
        -padding 0 -sticky nsew -state normal -text {Page 1} -image {} \
        -compound left -underline -1 
    set site_4_0  $top.tNo43.t0
    vTcl::widgets::ttk::scrolledtext::CreateCmd $site_4_0.scr49 \
        -background {#d9d9d9} -height 75 -highlightbackground {#d9d9d9} \
        -highlightcolor black -width 125 
    vTcl:DefineAlias "$site_4_0.scr49" "output" vTcl:WidgetProc "top_level" 1

    $site_4_0.scr49.01 configure -background white \
        -font font9 \
        -foreground black \
        -height 3 \
        -highlightbackground #d9d9d9 \
        -highlightcolor black \
        -insertbackground black \
        -insertborderwidth 3 \
        -selectbackground #c4c4c4 \
        -selectforeground black \
        -width 10 \
        -wrap none
    vTcl::widgets::ttk::scrolledtext::CreateCmd $site_4_0.scr50 \
        -background {#d9d9d9} -height 75 -highlightbackground {#d9d9d9} \
        -highlightcolor black -width 125 
    vTcl:DefineAlias "$site_4_0.scr50" "input" vTcl:WidgetProc "top_level" 1

    $site_4_0.scr50.01 configure -background white \
        -font font9 \
        -foreground black \
        -height 3 \
        -highlightbackground #d9d9d9 \
        -highlightcolor black \
        -insertbackground black \
        -insertborderwidth 3 \
        -selectbackground #c4c4c4 \
        -selectforeground black \
        -width 10 \
        -wrap none
    button $site_4_0.but51 \
        -activebackground {#ececec} -activeforeground {#000000} \
        -background {#d9d9d9} -command send_message \
        -disabledforeground {#a3a3a3} -font {-family {Segoe UI} -size 22} \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -pady 0 -text Send 
    vTcl:DefineAlias "$site_4_0.but51" "send_button" vTcl:WidgetProc "top_level" 1
    vTcl::widgets::ttk::scrolledlistbox::CreateCmd $site_4_0.scr52 \
        -background {#d9d9d9} -height 75 -highlightbackground {#d9d9d9} \
        -highlightcolor black -width 125 
    vTcl:DefineAlias "$site_4_0.scr52" "managers_list" vTcl:WidgetProc "top_level" 1

    $site_4_0.scr52.01 configure -background white \
        -disabledforeground #a3a3a3 \
        -font font10 \
        -foreground black \
        -height 3 \
        -highlightbackground #d9d9d9 \
        -highlightcolor #d9d9d9 \
        -selectbackground #c4c4c4 \
        -selectforeground black \
        -width 10
    label $site_4_0.lab53 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -disabledforeground {#a3a3a3} \
        -font {-family {Segoe UI} -size 18} -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -text Managers: 
    vTcl:DefineAlias "$site_4_0.lab53" "mangaers_label" vTcl:WidgetProc "top_level" 1
    label $site_4_0.lab54 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -disabledforeground {#a3a3a3} \
        -font {-family {Segoe UI} -size 18} -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -text Members: 
    vTcl:DefineAlias "$site_4_0.lab54" "members_label" vTcl:WidgetProc "top_level" 1
    vTcl::widgets::ttk::scrolledlistbox::CreateCmd $site_4_0.scr55 \
        -background {#d9d9d9} -height 75 -highlightbackground {#d9d9d9} \
        -highlightcolor black -width 125 
    vTcl:DefineAlias "$site_4_0.scr55" "mambers_list" vTcl:WidgetProc "top_level" 1

    $site_4_0.scr55.01 configure -background white \
        -disabledforeground #a3a3a3 \
        -font font10 \
        -foreground black \
        -height 3 \
        -highlightbackground #d9d9d9 \
        -highlightcolor #d9d9d9 \
        -selectbackground #c4c4c4 \
        -selectforeground black \
        -width 10
    button $site_4_0.but57 \
        -activebackground {#ececec} -activeforeground {#000000} \
        -background {#d9d9d9} -command un_mute -disabledforeground {#a3a3a3} \
        -font TkDefaultFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -pady 0 \
        -text Mute 
    vTcl:DefineAlias "$site_4_0.but57" "mute_button" vTcl:WidgetProc "top_level" 1
    button $site_4_0.but58 \
        -activebackground {#ececec} -activeforeground {#000000} \
        -background {#d9d9d9} -command kick -disabledforeground {#a3a3a3} \
        -font TkDefaultFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -pady 0 \
        -text Kick 
    vTcl:DefineAlias "$site_4_0.but58" "kick_button" vTcl:WidgetProc "top_level" 1
    button $site_4_0.but60 \
        -activebackground {#ececec} -activeforeground {#000000} \
        -background {#d9d9d9} -command appoint_manager \
        -disabledforeground {#a3a3a3} -font TkDefaultFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -pady 0 -text {Make Manager} 
    vTcl:DefineAlias "$site_4_0.but60" "appoint_button" vTcl:WidgetProc "top_level" 1
    button $site_4_0.but61 \
        -activebackground {#ececec} -activeforeground {#000000} \
        -background {#d9d9d9} -command add_user -disabledforeground {#a3a3a3} \
        -font TkDefaultFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -pady 0 \
        -text {Add User} 
    vTcl:DefineAlias "$site_4_0.but61" "add_button" vTcl:WidgetProc "top_level" 1
    place $site_4_0.scr49 \
        -in $site_4_0 -x 0 -y 0 -width 551 -relwidth 0 -height 431 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_4_0.scr50 \
        -in $site_4_0 -x 0 -y 438 -width 431 -relwidth 0 -height 61 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_4_0.but51 \
        -in $site_4_0 -x 436 -y 438 -width 117 -relwidth 0 -height 64 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_4_0.scr52 \
        -in $site_4_0 -x 557 -y 37 -width 211 -relwidth 0 -height 155 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_4_0.lab53 \
        -in $site_4_0 -x 552 -y 0 -width 116 -height 38 -anchor nw \
        -bordermode ignore 
    place $site_4_0.lab54 \
        -in $site_4_0 -x 552 -y 190 -width 112 -height 38 -anchor nw \
        -bordermode ignore 
    place $site_4_0.scr55 \
        -in $site_4_0 -x 558 -y 227 -width 211 -relwidth 0 -height 205 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_4_0.but57 \
        -in $site_4_0 -x 562 -y 438 -width 97 -relwidth 0 -height 24 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_4_0.but58 \
        -in $site_4_0 -x 669 -y 438 -width 97 -relwidth 0 -height 24 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_4_0.but60 \
        -in $site_4_0 -x 562 -y 474 -width 97 -relwidth 0 -height 24 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_4_0.but61 \
        -in $site_4_0 -x 669 -y 473 -width 97 -relwidth 0 -height 24 \
        -relheight 0 -anchor nw -bordermode ignore 
    frame $top.tNo43.t1 \
        -background {#d9d9d9} -highlightbackground {#d9d9d9} \
        -highlightcolor black 
    vTcl:DefineAlias "$top.tNo43.t1" "notebook_t1" vTcl:WidgetProc "top_level" 1
    $top.tNo43 add $top.tNo43.t1 \
        -padding 0 -sticky nsew -state normal -text {Page 2} -image {} \
        -compound left -underline -1 
    set site_4_1  $top.tNo43.t1
    button $top.but42 \
        -activebackground {#ececec} -activeforeground {#000000} \
        -background {#d9d9d9} -command new_room -disabledforeground {#a3a3a3} \
        -font TkDefaultFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -pady 0 -text + 
    vTcl:DefineAlias "$top.but42" "new_room_button" vTcl:WidgetProc "top_level" 1
    ###################
    # SETTING GEOMETRY
    ###################
    place $top.tNo43 \
        -in $top -x 0 -y 0 -width 784 -relwidth 0 -height 536 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.but42 \
        -in $top -x 47 -y 0 -width 19 -relwidth 0 -height 24 -relheight 0 \
        -anchor nw -bordermode ignore 

    vTcl:FireEvent $base <<Ready>>
}

set btop ""
if {$vTcl(borrow)} {
    set btop .bor[expr int([expr rand() * 100])]
    while {[lsearch $btop $vTcl(tops)] != -1} {
        set btop .bor[expr int([expr rand() * 100])]
    }
}
set vTcl(btop) $btop
Window show .
Window show .top42 $btop
if {$vTcl(borrow)} {
    $btop configure -background plum
}
