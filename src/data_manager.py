
import streamlit as st
import json
import pandas as pd
from datetime import datetime
import os

@st.cache_data(show_spinner=False)
def load_data(json_path=None):
    """Load the main JSON data. Trust data.json as source of truth."""
    try:
        # data/processed/data.json
        # Pointing to STAGING data
        prod_path = r"h:\VIBE CODE\ind basketball\2staging\data\processed\data.json"
        # Use json_path if provided, otherwise fallback to prod_path
        actual_path = json_path if json_path else prod_path
        
        if not os.path.exists(actual_path):
             actual_path = prod_path

        with open(actual_path, "r", encoding='utf-8-sig') as f:
            data = json.load(f)
            
        # Placeholder for total_games and last_updated
        if isinstance(data, dict):
            total_games = len(data.get("Matches", [])) if "Matches" in data else len(data.get("matches", []))
            # Fallback for flat list in dict wrapper
            if total_games == 0 and "matches" not in data and "Matches" not in data:
                 total_games = 0 # Structure unknown
        else:
            total_games = len(data)
            
        last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return data, total_games, last_updated
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return [], 0, "N/A"

@st.cache_data  
def load_category_map():
    """Load category map"""
    try:
        # Try both relative and absolute paths if needed, but relative usually works from root
        path = "data/raw/match_category_map.json"
        if not os.path.exists(path):
             path = r"h:\VIBE CODE\ind basketball\data\raw\match_category_map.json"
             
        with open(path, "r", encoding='utf-8-sig') as f:
            return json.load(f)
    except:
        return {}

@st.cache_data
def load_logos():
    try:
        path = "data/logos.json"
        if not os.path.exists(path):
             # Try prod path
             path = r"h:\VIBE CODE\ind basketball\2staging\data\logos.json" # Staging location
             if not os.path.exists(path):
                 path = r"h:\VIBE CODE\ind basketball\data\logos.json"

        with open(path, "r") as f:
            return json.load(f)
    except:
        return {}

def load_manual_scores():
    try:
        path = "data/processed/manual_scores.json"
        if not os.path.exists(path):
            path = r"h:\VIBE CODE\ind basketball\2staging\data\processed\manual_scores.json"
            
        with open(path, "r") as f:
            return json.load(f)
    except:
        return {}

def load_schedule():
    """Load the compiled schedule CSV"""
    try:
        # Point to production schedule
        schedule_path = r"h:\VIBE CODE\ind basketball\2staging\compiled_schedule.csv"
        df = pd.read_csv(schedule_path)
        return df
    except:
        return pd.DataFrame()
