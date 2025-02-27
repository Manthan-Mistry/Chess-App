import pandas as pd
import streamlit as st

from utils.functions import *

def show_senior_players():

    # Load and inject CSS into the Streamlit app

    # Get the base64-encoded image
    image_path = "assets/pawn_moving.png"
    image_base64 = get_base64_image(image_path)

    # Load and inject the CSS
    css = load_css("static/styles.css", image_base64)
    st.markdown(css, unsafe_allow_html=True)

    df = sr_data()

    player_df = pd.read_csv('data/all_player_info.csv')
    
    # Player Name : Username
    players_dict = {
        'Magnus Carlsen':'MagnusCarlsen',
        'Hikaru Nakamura':'Hikaru',
        'Fabiano Caruana':'FabianoCaruana',
        'Arjun Erigaisi':'ArjunErigaisi2003',
        'Ian Nepomniatchi':'lachesisQ',
        'Gukesh D.':'GukeshDommaraju',
        'Nodirbek Abdusattarov':'ChessWarrior7197',
        'Wei Yein':'LOVEVAE',
        'Alireza Firouzja':'Firouzja2003',
        'Wesley So':'GMWSO',
        'Pragnananddha R':'rpragchess',
        'Lenieay Dominguez':'DominguezOnYoutube',
        'Anish Giri':'AnishGiri',
        'Ding Liren':'Chefshouse'
        }
    
 # Adjust the column name as needed
    game_time_classes = ['All', 'rapid', 'blitz','bullet'] # Adjust the column name as needed

    win_conditions = ['win']
    lose_conditions = ['resigned', 'checkmated', 'timeout', 'abandoned']
    draw_conditions = ['agreed', 'stalemate', '50move','repetition','timevsinsufficient','insufficient']

    # Create two columns for the dropdowns
    col1, col2 = st.columns([1,1])

    with col1:
        # Dropdown for selecting a player
        selected_playername = st.selectbox('Select Player', list(players_dict.keys()), key='player')
        selected_player = players_dict[selected_playername]
        st.session_state.selected_player = selected_player


    with col2:
        # Dropdown for selecting game time class
        selected_game_time_class = st.selectbox('Select Game Time Class', game_time_classes, key='game_time_class')
        st.session_state.selected_game_time_class = selected_game_time_class

    if selected_game_time_class == 'All':
        temp_df = df[((df['white_username'] == st.session_state.selected_player) | (df['black_username'] == st.session_state.selected_player))]
    else:
        temp_df = df[((df['white_username'] == st.session_state.selected_player) | (df['black_username'] == st.session_state.selected_player)) & (df['game_time_class'] == st.session_state.selected_game_time_class)]
        

    # Create separate DataFrames for wins, draws, and losses
    win_df = temp_df[((temp_df['white_username'] == st.session_state.selected_player) & (temp_df['white_result'].isin(win_conditions))) |
                    ((temp_df['black_username'] == st.session_state.selected_player) & (temp_df['black_result'].isin(win_conditions)))]

    draw_df = temp_df[((temp_df['white_username'] == st.session_state.selected_player) & (temp_df['white_result'].isin(draw_conditions))) |
                    ((temp_df['black_username'] == st.session_state.selected_player) & (temp_df['black_result'].isin(draw_conditions)))]

    loss_df = temp_df[((temp_df['white_username'] == st.session_state.selected_player) & (temp_df['white_result'].isin(lose_conditions))) |
                    ((temp_df['black_username'] == st.session_state.selected_player) & (temp_df['black_result'].isin(lose_conditions)))]

    (total_games, white_accuracy, black_accuracy,
    wins_as_white, loss_as_white, draws_as_white, total_games_white, white_win_ratio, white_loss_ratio, white_draw_ratio,
    wins_as_black, loss_as_black, draws_as_black, total_games_black, black_win_ratio, black_loss_ratio, black_draw_ratio,
    opening_lines,white_most_played_openings, white_most_accurate_openings, black_most_played_openings, black_most_accurate_openings) = display_player_stats(temp_df, selected_player)

    profile_df = pd.read_csv('data/new_sr_players_avatar2.csv')

    with st.container():
        avatar_url_main = get_player_avatar(profile_df, selected_player) or "https://images.chesscomfiles.com/uploads/v1/master_player/31312204-98ce-11eb-a526-bf8e17d64341.9d09bea2.250x250o.aa644e468977.jpg"

        player_row = player_df[player_df['Username'] == selected_player.lower()].iloc[0]

        title = player_row['Title']
        name = player_row['Name']
        username = player_row['Username']
        country_code = get_country_code(player_row['Country'])
        location = player_row['Location']
        last_online = pd.to_datetime(list(temp_df.sort_values('game_date', ascending = False)[:1]['game_date'])[0]).strftime('%b %d, %Y')
        joined = pd.to_datetime(player_row['Joined'], unit='s').strftime('%b %d, %Y')
        followers = "{:,}".format(player_row['Followers'])
        is_streamer = "💎" if player_row['Verified'] else ""

        # Bootstrap CSS and Icons CDN
        st.markdown("""
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css" rel="stylesheet">
        """, unsafe_allow_html=True)


        # Player-Info CSS Styles:
        st.write(
        f"""
        <div class="profile-container">
            <div style="display: flex; justify-content: left;">
                <img src="{avatar_url_main}" style="border-radius: 10%; border: 2px solid #69923e; width: 150px; margin-top: 5px;">
            </div>
            <div class="player-info">
                <div class="name-section">
                    <div class="title">{title}</div>
                    <div class="player-name">{username}</div>
                    <div class="country-flag">
                        <img src="https://flagcdn.com/40x30/{country_code.lower()}.png" alt="Country Flag"> 
                    </div>
                    <div class="badge">💎</div>
                </div>
                <div class="full-name-location">
                    {name} <span class = "bi bi-geo-alt-fill" style = "font-size: 0.8rem; margin-left: 20px;"></span> {location}
                </div>
                <div class="additional-info">
                    <div class="info-box">
                        <div class="bi bi-activity" style = "font-size: 1.2rem; font-weight: bold; margin-left: 10px;"></div>
                        Online on:<br> <span style = "margin-left: 5px;">{last_online} </span>
                    </div>
                    <div class="info-box">
                        <div class="bi bi-calendar" style = "font-size: 1rem; font-weight: bold; margin-left: 10px;"></div>
                         Joined on:<br> <span style = "margin-left: 5px;">{joined} </span>
                    </div>
                    <div class="info-box">
                        <div class="bi bi-people-fill" style = "font-size: 1.2rem; font-weight: bold; margin-left: 10px;"></div>
                        Followers:<br> <span style = "margin-left: 5px;">{followers} </span>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

        st.write('') ## Margin setting :)
        st.write('')
        st.write('')
        
        col1, col2, col3 = st.columns(3, gap = 'large')

        with col1:
            st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-label">Total Games <br> </div>
                    <div class="metric-value">{total_games}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.write('')

        with col2:
            st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-label">Avg Accuracy as White <br> </div>
                    <div class="metric-value"> {white_accuracy:.2f}%</div>
                </div>
                """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-label">Avg Accuracy as Black <br> </div>
                    <div class="metric-value">{black_accuracy:.2f}%</div>
                </div>
                """, unsafe_allow_html=True)
            
    col1, col2, col3 = st.columns(3, gap = 'large')

    with col1:
        avg_rating = calculate_avg_opponent_rating(temp_df, st.session_state.selected_player)
        st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-label">Avg Opponent Rating</div>
                    <div class="metric-value">{round(avg_rating)}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.write('')

    with col2:
        # Calculate the best win for the selected player
        best_opponent_name, best_opponent_rating = get_best_win(df, st.session_state.selected_player, win_conditions)

        if best_opponent_name is not None and best_opponent_rating is not None:
            st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-label">Best Win</div>
                    <div class="metric-value">{best_opponent_rating}</div>
                    <div class="metric-delta">{best_opponent_name}</div>
                </div>
                """, unsafe_allow_html=True)

    with col3:
        # Calculate average opponent ratings for wins, draws, and losses
        avg_rating_win = calculate_avg_opponent_rating(win_df, st.session_state.selected_player)
        avg_rating_draw = calculate_avg_opponent_rating(draw_df, st.session_state.selected_player)
        avg_rating_loss = calculate_avg_opponent_rating(loss_df, st.session_state.selected_player)

        win_png = load_image("assets/win3.png")  
        draw_png = load_image("assets/draw2.png")  
        loss_png = load_image("assets/loss2.png")  

        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label-spec">Avg Opponent Rating <br> when player...</div>
                <div class="metric-value-spec">
                    <span class="value-win">
                        <img src="data:image/png;base64,{win_png}" width="18" height="18" style="vertical-align: middle; margin-bottom: 5px;"/> {round(avg_rating_win)}
                    </span>
                    <span class="value-draw">
                        <img src="data:image/png;base64,{draw_png}" width="18" height="18" style="vertical-align: middle; margin-bottom: 5px;"/> {round(avg_rating_draw)}
                    </span>
                    <span class="value-loss">
                        <img src="data:image/png;base64,{loss_png}" width="18" height="18" style="vertical-align: middle; margin-bottom: 5px;"/> {round(avg_rating_loss)}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # https://discuss.streamlit.io/t/display-svg/172/5 --> code reference.
        
    col1, col2, col3 = st.columns(3, gap = 'large')

    with col1:
        rapid_img = load_image('assets/stopwatch.png')
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-icon" style="margin-right: 10px;">
                    <img src="data:image/png;base64,{rapid_img}" style="width: 16px; height: 16px;">
                </div>
                <div class="metric-label">Best Rapid Rating <br> </div>
                <div class="metric-value">{get_game_class_rating(df, selected_player, 'rapid')}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.write('')

    with col2:
        blitz_image = load_image('assets/flash.png')
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-icon" style="margin-right: 10px;">
                    <img src="data:image/png;base64,{blitz_image}" style="width: 18px; height: 18px;">
                </div>
                <div class="metric-label">Best Blitz Rating <br> </div>
                <div class="metric-value"> {get_game_class_rating(df, selected_player, 'blitz')}</div>
            </div>
            """, unsafe_allow_html=True)
        
    with col3:
        bullet_image = load_image("assets/bullet3.png")
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-icon" style="margin-right: 10px;">
                    <img src="data:image/png;base64,{bullet_image}" style="width: 18px; height: 18px;">
                </div>
                <div class="metric-label">Best Bullet Rating <br> </div>
                <div class="metric-value">{get_game_class_rating(df, selected_player, 'bullet')}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.write('') ## Margin setting :)
        st.write('')
        st.write('')

    col1, col2, col3 = st.columns(3, gap='large')
    with col1:
        st.plotly_chart(player_win_chart(df, selected_player, 400, 300),  config={'displayModeBar': False}, key = 'pie')
        image_path = 'assets/Pie Chart Legend (1).png'
        st.write('')
        st.image(image = image_path, width= 365)

    with col2:
        st.plotly_chart(player_draw_chart(df, selected_player, 400, 300),  config={'displayModeBar': False}, key = 'pie')
        image_path = 'assets/New Draw Pie Chart Legend (1).png'
        st.write('')
        st.image(image = image_path, width= 365)

    with col3:
        st.plotly_chart(player_loss_chart(df, selected_player, 400 , 300),  config={'displayModeBar': False}, key = 'pie')
        image_path = 'assets/Lose Pie Chart Legend.png'
        st.write('')
        st.image(image = image_path, width= 365)

    if 'tab_selected' not in st.session_state:
        st.session_state.tab_selected = 'white'
        
    # Create Tabs for White and Black stats
    tab_white, tab_black = st.tabs(["⬜ White", "⬛ Black"])

    # Tab for White Stats
    with tab_white:
        st.session_state.tab_selected = 'white'

        #Show Player as White Stats:
        show_white_stats(total_games_white, white_win_ratio, white_draw_ratio, white_loss_ratio, wins_as_white, draws_as_white, loss_as_white, white_most_accurate_openings, white_most_played_openings)

    with tab_black:
        st.session_state.tab_selected = 'black'

        #Show Player as Black Stats:
        show_black_stats(total_games_black, black_win_ratio, black_draw_ratio, black_loss_ratio, wins_as_black, draws_as_black, loss_as_black, black_most_accurate_openings, black_most_played_openings)

    render_rating_chart_with_tabs(df, selected_playername=selected_playername, selected_player=selected_player, players_dict=players_dict, width=1180, height=400)
    st.caption("Note: The rating curve shown is smoothed using a rolling average to provide a clearer trend. The highest rating annotation reflects the actual unsmoothed rating.")
