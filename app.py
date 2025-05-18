import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import os
import time

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'team_name' not in st.session_state:
    st.session_state.team_name = None
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'end_time' not in st.session_state:
    st.session_state.end_time = None
if 'current_card' not in st.session_state:
    st.session_state.current_card = 1
if 'completed_cards' not in st.session_state:
    st.session_state.completed_cards = []
if 'previous_answers' not in st.session_state:
    st.session_state.previous_answers = []
if 'time_up' not in st.session_state:
    st.session_state.time_up = False

# Team credentials
TEAM_CREDENTIALS = {
    "Krishna": {"password": "team1", "cards": [
        {"trait": "Strategic", "riddle": "I look ahead, beyond today,\nTo plan and pave a smarter way.\nVision is key, I plot with grace,\nWhat am I in this CEO race?", "answer": "Strategic", "location": "Location 1"},
        {"trait": "Understanding", "riddle": "I listen close, I care, I feel,\nI value thoughts that others reveal.\nThrough empathy, I lead with might,\nWhat makes my leadership so right?", "answer": "Understanding", "location": "Location 2"},
        {"trait": "Nimble", "riddle": "In a tech world changing every hour,\nI shift with speed and mental power.\nI don't stay stuck, I swiftly act,\nWhat trait helps keep my plans intact?", "answer": "Nimble", "location": "Location 3"},
        {"trait": "Decisive", "riddle": "In moments when the stakes are high,\nI choose the best without a sigh.\nI don't delay or second guess,\nWhat trait helps me face the stress?", "answer": "Decisive", "location": "Location 4"},
        {"trait": "Analytical", "riddle": "Data, numbers, charts and lines,\nI read the clues and spot the signs.\nMy brain breaks down the complex things,\nWhat skill is key to what success brings?", "answer": "Analytical", "location": "Location 5"},
        {"trait": "Resilient", "riddle": "I rise when failures bring me down,\nI fight again without a frown.\nThrough thick and thin, I never bend,\nWhat trait helps me transcend?", "answer": "Resilient", "location": "Location 6"}
    ]},
    "Brahmaputra": {"password": "team2", "cards": [
        {"trait": "Strategic", "riddle": "I look ahead, beyond today,\nTo plan and pave a smarter way.\nVision is key, I plot with grace,\nWhat am I in this CEO race?", "answer": "Strategic", "location": "Location 1"},
        {"trait": "Adaptive", "riddle": "The world may shift, the tech may change,\nBut I adjust within that range.\nI flex, I flow, I find my way,\nWhat trait helps me win the day?", "answer": "Adaptive", "location": "Location 2"},
        {"trait": "Thoughtful", "riddle": "I care before I speak or do,\nI think of others' point of view.\nWith gentle strength, I lead the way,\nWhat's this trait I show each day?", "answer": "Thoughtful", "location": "Location 3"},
        {"trait": "Youthful", "riddle": "Though age may rise, I still embrace,\nNew ways, bold dreams, a forward pace.\nWith energy and open mind,\nWhat trait helps me stay aligned?", "answer": "Youthful", "location": "Location 4"},
        {"trait": "Authentic", "riddle": "I stay true to who I am,\nI don't pretend or give a sham.\nWith honesty and steady tone,\nWhat makes my voice my own?", "answer": "Authentic", "location": "Location 5"}
    ]},
    "Ganga": {"password": "team3", "cards": [
        {"trait": "Nurturing", "riddle": "I guide with warmth and help them grow,\nI cheer the highs and help the lows.\nI mentor, coach, and always care —\nWhat trait shows I'm always there?", "answer": "Nurturing", "location": "Location 1"},
        {"trait": "Assertive", "riddle": "I speak my mind, I'm bold and clear,\nI chase the truth, I have no fear.\nMy tone is strong, my stance is fair —\nWhat trait shows I truly care?", "answer": "Assertive", "location": "Location 2"},
        {"trait": "Motivational", "riddle": "With words and will, I lift the team,\nI fuel their fire, I boost their dream.\nA cheer, a push, a hopeful view —\nWhat trait helps them follow through?", "answer": "Motivational", "location": "Location 3"},
        {"trait": "Intelligent", "riddle": "Ideas spark and numbers fly,\nI solve with reason, not just try.\nLogic, facts, and insight too —\nWhat trait defines my point of view?", "answer": "Intelligent", "location": "Location 4"},
        {"trait": "Transparent", "riddle": "No hidden games, no sugarcoat,\nI speak the truth, I take the vote.\nWith honesty, I lead the lane —\nWhat trait helps me stay so plain?", "answer": "Transparent", "location": "Location 5"},
        {"trait": "Ambitious", "riddle": "I dream big, I aim so high,\nI won't stop till I touch the sky.\nGoals are more than what they seem —\nWhat trait defines my burning dream?", "answer": "Ambitious", "location": "Location 6"}
    ]},
    "Tungabhadra": {"password": "team4", "cards": [
        {"trait": "Leadership", "riddle": "I lead the way, I clear the fog,\nI steer the ship through any slog.\nWith vision wide and actions neat,\nWhat trait helps me guide my fleet?", "answer": "Leadership", "location": "Location 1"},
        {"trait": "Empathy", "riddle": "Your pain, your joy, I understand,\nI help you up, I hold your hand.\nI see your side and walk your way,\nWhat's this trait that makes my day?", "answer": "Empathy", "location": "Location 2"},
        {"trait": "Ethical", "riddle": "Right or wrong, I choose the right,\nI never hide, I walk in light.\nMy code is strong, I never fall —\nWhat trait defines my moral call?", "answer": "Ethical", "location": "Location 3"},
        {"trait": "Non-judgmental", "riddle": "I accept all paths, all points of view,\nI let you be just you, not new.\nI welcome thoughts, both big and small,\nWhat trait helps me hear them all?", "answer": "Non-judgmental", "location": "Location 4"},
        {"trait": "Authentic", "riddle": "I'm myself — not fake, not dressed,\nI speak my truth, I show my best.\nNo mask, no filter, just my core —\nWhat trait helps me lead and soar?", "answer": "Authentic", "location": "Location 5"}
    ]}
}

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def login_page():
    st.title("Treasure Hunt Login")
    
    team_name = st.selectbox("Select your team", ["Krishna", "Brahmaputra", "Ganga", "Tungabhadra"])
    password = st.text_input("Enter team password", type="password")
    
    if st.button("Login"):
        if team_name in TEAM_CREDENTIALS and password == TEAM_CREDENTIALS[team_name]["password"]:
            st.session_state.authenticated = True
            st.session_state.team_name = team_name
            st.session_state.start_time = datetime.now()
            st.session_state.end_time = st.session_state.start_time + timedelta(minutes=15)
            st.session_state.time_up = False
            st.rerun()
        else:
            st.error("Invalid credentials!")

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"

def display_timer():
    if st.session_state.start_time and not st.session_state.time_up:
        current_time = datetime.now()
        time_left = (st.session_state.end_time - current_time).total_seconds()
        
        if time_left <= 0:
            st.session_state.time_up = True
            return "00:00"
        
        return format_time(int(time_left))
    return "00:00"

def show_animation(message, is_success=True):
    if is_success:
        st.markdown(f"""
        <div style='background-color: #d4edda; color: #155724; padding: 10px; border-radius: 5px; margin: 10px 0;'>
            ✅ {message}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='background-color: #f8d7da; color: #721c24; padding: 10px; border-radius: 5px; margin: 10px 0;'>
            ❌ {message}
        </div>
        """, unsafe_allow_html=True)

def display_previous_answers():
    # This function is no longer needed as we've moved the display logic to the game page
    pass

def game_page():
    st.title(f"Team {st.session_state.team_name}'s Treasure Hunt")
    
    # Display countdown timer
    timer_container = st.empty()
    timer_container.markdown(f"⏱️ Time Remaining: **{display_timer()}**")
    
    # Check if time is up
    if st.session_state.time_up:
        st.error("⏰ Time's up! The game is over.")
        st.stop()
    
    # Get current card
    current_card = st.session_state.current_card
    team_cards = TEAM_CREDENTIALS[st.session_state.team_name]["cards"]
    
    if current_card <= len(team_cards):
        card = team_cards[current_card - 1]
        
        st.subheader(f"Card {current_card}")
        st.write("Riddle:")
        st.markdown(f"""
        <div style='background-color: #2b2b2b; color: #ffffff; padding: 20px; border-radius: 10px; margin: 10px 0; font-size: 1.1em; line-height: 1.6; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            {card['riddle']}
        </div>
        """, unsafe_allow_html=True)
        
        answer = st.text_input("Enter your answer:")
        
        if st.button("Submit Answer"):
            if answer.lower() == card['answer'].lower():
                # Add to previous answers
                st.session_state.previous_answers.append({
                    'card_number': current_card,
                    'trait': card['trait'],
                    'answer': card['answer'],
                    'location': card['location']
                })
                
                show_animation("Correct! Here's the location of your next clue:")
                st.markdown(f"""
                <div style='background-color: #d4edda; color: #155724; padding: 15px; border-radius: 8px; margin: 10px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                    📍 Location: {card['location']}
                </div>
                """, unsafe_allow_html=True)
                
                st.session_state.completed_cards.append(current_card)
                st.session_state.current_card += 1
                time.sleep(2)  # Give time to see the success message
                st.rerun()
            else:
                show_animation("Incorrect answer. Try again!", is_success=False)
        
        # Display previous answers below the input box
        if st.session_state.previous_answers:
            st.markdown("---")  # Add a separator
            st.subheader("Completed Cards")
            for card in st.session_state.previous_answers:
                # Create the base card display
                card_html = f"""
                <div style='background-color: #e8f4f8; color: #2c3e50; padding: 15px; border-radius: 8px; margin: 8px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                    <strong>Card {card['card_number']}:</strong> {card['answer']}
                """
                
                # Add location if it exists
                if 'location' in card:
                    card_html += f"<br><span style='color: #666; font-size: 0.9em;'>📍 {card['location']}</span>"
                
                card_html += "</div>"
                st.markdown(card_html, unsafe_allow_html=True)
    else:
        st.success("🎉 Congratulations! You have completed all the cards!")
    
    # Auto-refresh the page every second to update the timer
    time.sleep(1)
    st.rerun()

def admin_page():
    st.title("Admin Dashboard")
    
    username = st.text_input("Admin Username")
    password = st.text_input("Admin Password", type="password")
    
    if st.button("Login as Admin"):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.authenticated = True
            st.session_state.is_admin = True
            st.rerun()
        else:
            st.error("Invalid admin credentials!")

def admin_dashboard():
    st.title("Admin Dashboard")
    
    # Create a DataFrame for team progress
    progress_data = []
    for team in TEAM_CREDENTIALS:
        start_time = st.session_state.get(f"{team}_start_time")
        time_left = "N/A"
        if start_time:
            end_time = start_time + timedelta(minutes=15)
            time_left = format_time(int((end_time - datetime.now()).total_seconds()))
        
        progress_data.append({
            "Team": team,
            "Cards Completed": len(st.session_state.get(f"{team}_completed_cards", [])),
            "Total Cards": len(TEAM_CREDENTIALS[team]["cards"]),
            "Current Card": st.session_state.get(f"{team}_current_card", 1),
            "Time Remaining": time_left
        })
    
    df = pd.DataFrame(progress_data)
    st.dataframe(df, use_container_width=True)
    
    # Display detailed progress for each team
    for team in TEAM_CREDENTIALS:
        st.subheader(f"Team {team} Progress")
        completed_cards = st.session_state.get(f"{team}_completed_cards", [])
        st.write(f"Completed Cards: {completed_cards}")
        st.write(f"Current Card: {st.session_state.get(f'{team}_current_card', 1)}")

def main():
    if not st.session_state.authenticated:
        tab1, tab2 = st.tabs(["Team Login", "Admin Login"])
        
        with tab1:
            login_page()
        with tab2:
            admin_page()
    else:
        if st.session_state.get("is_admin", False):
            admin_dashboard()
        else:
            game_page()

if __name__ == "__main__":
    main() 