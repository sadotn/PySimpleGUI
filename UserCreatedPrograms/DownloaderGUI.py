import PySimpleGUI as sg

app_title = 'Hanash Download Manager'
themes = list(sg.LOOK_AND_FEEL_TABLE.keys())
sg.ChangeLookAndFeel('Green')
sg.SetOptions(font='Helvetica 11', auto_size_buttons=True, progress_meter_border_depth=0, border_width=1)

# region gui design
def create_window():
    # main tab
    main_layout = [[sg.T('', size=(14, 1), font='Helvetica 11'), sg.Text('Hanash Download Manager', font='Helvetica 20'),
                        sg.T(' ', size=(8, 1)), sg.Button('info', key='about')],

                       # url
                       [sg.Text('URL:')],
                       [sg.Input('', enable_events=True, change_submits=True, key='url', size=(68, 1)),
                        sg.Button('Retry')],
                       [sg.Text('Status:', size=(70, 1), key='status')],

                   # spacer
                   [sg.T('', font='any 1')],

                   # youtube playlist
                   [sg.Frame('Youtube Playlist / videos:', layout=[
                       [sg.Combo(values=['Playlist'], size=(30, 1), key='pl_menu', enable_events=True),
                        sg.Button('v', tooltip='download this playlist', key='pl_download'),
                        sg.Combo(values=['Quality'], size=(30, 1), key='stream_menu', enable_events=True)],

                       # progress bars
                       [sg.ProgressBar(max_value=100, size=(24, 5), key='m_bar'), sg.T(' ' * 7, font='Helvetica 9'),
                        sg.ProgressBar(max_value=100, size=(24, 5), key='s_bar')],

                   ])],

                   # file info
                   [sg.Text('File name:'), sg.Input('', size=(65, 1), key='name', enable_events=True)],
                   [sg.T('File size:'), sg.T(' ' * 30, key='size'), sg.T('Type:'), sg.T(' ' * 35, key='type'),
                    sg.T('Resumable'), sg.T(' ' * 5, key='resumable')],
                   [sg.Text('Save To:'), sg.Input('Downloads', size=(57, 1), key='folder', enable_events=True),
                    sg.FolderBrowse(key='browse')],

                   # download button
                   [sg.T('', size=(27, 1), font='Helvetica 11'), sg.Button('Download', font='Helvetica 14', border_width=1)],

                   ]

    # downloads tab
    d_headers = ['i', 'num', 'name', 'progress', 'speed', 'time_left', 'size', 'downloaded', 'status',
                 'resumable', 'folder', 'max_connections', 'live_connections', 'remaining_parts']

    spacing = [' ' * 4, ' ' * 3, ' ' * 30, ' ', ' ' * 8, ' ' * 8, ' ' * 8, ' ' * 8, ' ' * 10, ' ' * 12, ' ', ' ',
               ' ', ' ']  # setup initial column width

    downloads_layout = [[sg.Button('Resume'), sg.Button('Cancel'), sg.Button('Refresh'),
                         sg.Button('Folder'), sg.Button('D.Window'),
                         sg.T(' ' * 5), sg.T('Item:'),
                         sg.T('---', key='selected_row_num', text_color='white', background_color='red')],
                        [sg.Table(values=[spacing], headings=d_headers, size=(70, 13),
                                  vertical_scroll_only=False, key='table', enable_events=True)],
                        [sg.Button('Resume All'), sg.Button('Stop All'),
                         sg.Button('Delete', button_color=('white', 'red')),
                         sg.Button('Delete All', button_color=('white', 'red'))],
                        ]

    # setting tab
    setting_layout = [[sg.T('Setting:')],
                      [sg.Text('Select Theme:'),
                       sg.Combo(values=themes, default_value='Green', size=(15, 1), enable_events=True,
                                key='themes')],
                      [sg.T('Speed Limit:'), sg.Input('', size=(4, 1), key='speed_limit', enable_events=True),
                       sg.T('kb/s')],
                      [sg.Checkbox('Monitor copied urls in clipboard', default=True, key='monitor',enable_events=True)],
                      [sg.Checkbox("Don't show download window", key='hide_download_window',
                                   default=False, enable_events=True)],
                      [sg.Text('Max concurrent downloads:'),
                       sg.Combo(values=[x for x in range(1, 101)], size=(5, 1), enable_events=True,
                                key='max_concurrent_downloads', default_value=3)],
                      [sg.Text('Max connections per download:'),
                       sg.Combo(values=[x for x in range(1, 101)], size=(5, 1), enable_events=True,
                                key='max_connections', default_value=10)],
                      [sg.Text('file part size:'), sg.Input(default_text=1024, size=(6, 1), enable_events=True,
                                                            key='part_size'), sg.Text('KBytes')],
                      ]

    log_layout = [[sg.T('Details events:')], [sg.Multiline(default_text='', size=(70, 16), key='log')],
                  [sg.Button('Clear Log')]]

    layout = [[sg.TabGroup(
        [[sg.Tab('Main', main_layout), sg.Tab('Downloads', downloads_layout), sg.Tab('Setting', setting_layout),
          sg.Tab('Log', log_layout)]],
        key='tab_group')],
        [sg.StatusBar('', size=(75, 1), key='status_bar')]
    ]

    # window
    return sg.Window(title=app_title, layout=layout, size=(700, 450))

window = create_window()

while True:
    event, values = window.Read(timeout=50)

    if event is None:
        window.Close()
        break
    elif event == 'themes':
        sg.ChangeLookAndFeel(values['themes'])
        # restart window to apply new theme
        window.Close()
        window = create_window()
