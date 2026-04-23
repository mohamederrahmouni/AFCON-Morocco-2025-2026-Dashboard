#importing libraries
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.metric_cards import style_metric_cards
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(page_title="AFCON Morocco 2025-2026 Dashboard",page_icon=":soccer:",layout="wide",initial_sidebar_state="expanded")

afcon=pd.read_csv(r"C:\Users\dell\Desktop\AFCON_Dashboard\AFCON-2025-Matches-Stats.csv")
players=pd.read_csv(r"C:\Users\dell\Desktop\AFCON_Dashboard\AFCON-2025-Players-Stats.csv")
team_stat = pd.concat([afcon[["team1","team1_goals","team1_shots","team1_shots_on_target","team1_possession","team1_fouls","team1_red_cards","team1_yellow_cards"]].rename(columns={"team1":"Team","team1_goals":"Goals","team1_shots":"Shots","team1_shots_on_target":"Shots on target","team1_possession":"Possession","team1_fouls":"Fouls","team1_red_cards":"Red cards","team1_yellow_cards":"Yellow cards"}),afcon[["team2","team2_goals","team2_shots","team2_shots_on_target","team2_possession","team2_fouls","team2_red_cards","team2_yellow_cards"]].rename(columns={"team2": "Team","team2_goals":"Goals","team2_shots":"Shots","team1_shots_on_target":"Shots on target","team2_possession":"Possession","team2_fouls":"Fouls","team2_red_cards":"Red cards","team2_yellow_cards":"Yellow cards"})],axis=0)


opt_menu=option_menu(menu_title="Main menu",options=["Home","Competition Overview","Dashboard"],icons=["house","eye","graph-up"],menu_icon="cast",default_index=0,orientation="horizontal")
st.divider()

# Main menu
if opt_menu =="Home":
 st.markdown("<h1 style='text-align: center;'>Welcome to the AFCON Morocco 2025 Dashboard</h1>",unsafe_allow_html=True)
 st.divider()
 st.image(r"C:\Users\dell\Desktop\AFCON_Dashboard\Pictures\AFCON_logo.png",use_container_width=True)

 col1,col2=st.columns(2)
 with col1:
  st.image(r"C:\Users\dell\Desktop\AFCON_Dashboard\Pictures\Img1.jpeg",use_container_width=True)

 with col2:
  st.image(r"C:\Users\dell\Desktop\AFCON_Dashboard\Pictures\Img2.jpeg",use_container_width=True)

#Africa cup overview
elif opt_menu == "Competition Overview":
 total_team=team_stat["Team"].nunique()
 stadium_number=afcon["stadium_name"].nunique()
 total_matches=afcon.shape[0]
 total_goals=int(team_stat["Goals"].sum())
 total_attendance=int(afcon["attendance"].sum())
 c1,c2,c3,c4,c5=st.columns(5)
 c1.metric(label="Qualified teams",value=total_team)
 c2.metric(label="Number of stadiums",value=stadium_number)
 c3.metric(label="Total matches",value=total_matches)
 c4.metric(label="Total goals",value=total_goals)
 c5.metric(label="Total attendance",value=total_attendance)
 style_metric_cards(background_color="#199D28",border_left_color="red",box_shadow=True)

 st.divider()
 
 col1,col2=st.columns(2)
 with col1:
  st.subheader("Distribution of matches per stadiums")
  fig1=px.pie(afcon,names="stadium_name",labels={"stadium_name":"Stadium"},hole=0.4)
  fig1.update_layout(showlegend=True,template="simple_white",width=900,legend_title_text="Stadium :")
  fig1.update_traces(textinfo="percent",marker_line_color="black",marker_line_width=0.5)
  st.plotly_chart(fig1,use_container_width=True)
 
 
 with col2:
  st.markdown('<div class="card">', unsafe_allow_html=True)
  st.subheader("Distribution of Goals per stage ")
  group_stage=["Matchday 1","Matchday 2","Matchday 3"]
  group_stage_goals=afcon[afcon["Game Week"].isin(group_stage)]["total_goals"].sum()
  Knockout_stage_goals=afcon[afcon["Game Week"]=="Knockout Stage"]["total_goals"].sum()
  stage=["Group Stage","Knockout Stage"]
  goals=[int(group_stage_goals),int(Knockout_stage_goals)]
  fig2=px.bar(x=stage,y=goals,color_discrete_sequence=["#34ebe8"],labels={"y":"Goals"},text_auto=True)
  fig2.update_layout(xaxis_title="Stages",yaxis_title="Goals",bargap=0.3,xaxis_title_font=dict(size=15,color="white"),yaxis_title_font=dict(size=15,color="white"))
  fig2.update_traces(marker_line_color='black',marker_line_width=1)
  st.plotly_chart(fig2,use_container_width=True)
  st.markdown('</div>', unsafe_allow_html=True)

 st.divider()

#filtering goals by date
 d1,d2=st.columns(2)
 afcon["date"]=pd.to_datetime(afcon["date"]).dt.date
 start_date=pd.to_datetime(afcon["date"]).min()
 end_date=pd.to_datetime(afcon["date"]).max()

 with d1:
    date1=st.date_input("Start Date",start_date)
  
 with d2:
    date2=st.date_input("End Date",end_date)

 df_date=afcon[(afcon["date"] >= date1) & (afcon["date"] <= date2)].copy()

 st.subheader("Total goals over time")
 time_goals=df_date.groupby("date")["total_goals"].sum()
 fig3=px.line(time_goals,markers=False,labels={"value":"Goals"})
 fig3.update_layout(xaxis_title="Match date",yaxis_title="Goals",template="gridon",showlegend=False,xaxis_title_font=dict(size=15,color="white"),yaxis_title_font=dict(size=15,color="white"))
 st.plotly_chart(fig3,use_container_width=True)
 
 st.divider()

 st.markdown("<h1 style='text-align: center;'>Matches statistics</h1>",unsafe_allow_html=True) 
 st.markdown(" ")
 st.dataframe(afcon)

#main dashboard
else:
  st.markdown("""<style>button[data-baseweb="tab"] {font-size: 10px;padding: 10px 30px;}</style>""", unsafe_allow_html=True)
  tab1,tab2,tab3=st.tabs(["Goals","Teams","Players"])

## Goals dashboard 
  with tab1 :
   st.markdown("<h2 style='text-align: center;'>Goals Distribution</h2>",unsafe_allow_html=True)
   col1,col2=st.columns(2)
   with col1:
    st.subheader("Distribution of Goals per matches")
    fig4=px.histogram(afcon,x="total_goals",color_discrete_sequence=["#02C92A"]) 
    fig4.update_layout(xaxis_title="Total Goals",yaxis_title="Number of matches",bargap=0.2,width=1000,height=500,xaxis_title_font=dict(color="white",size=15),yaxis_title_font=dict(color="white",size=15))
    fig4.update_traces(marker_line_color='black',marker_line_width=1)
    st.plotly_chart(fig4,use_container_width=True)
   with col2:
    st.subheader("Distribution of goals in each stadiums")
    stadium_goals=afcon.groupby("stadium_name")["total_goals"].sum().sort_values()
    fig5=px.bar(stadium_goals,color_discrete_sequence=["#9d76cc"],orientation="h",labels={"value":"Goals","stadium_name":"Stadium"},text_auto=True) 
    fig5.update_layout(xaxis_title="Total Goals",yaxis_title="Stadium",bargap=0.2,width=1000,height=500,showlegend=False,xaxis_title_font=dict(size=15,color="white"),yaxis_title_font=dict(size=15,color="white"))
    fig5.update_traces(marker_line_color='black',marker_line_width=1)
    st.plotly_chart(fig5,use_container_width=True)

   st.divider()

   st.markdown("<h2 style='text-align: center;'>Offensive efficiency</h2>",unsafe_allow_html=True)
   c3,c4=st.columns(2)
   with c3:
    st.subheader("Goals scored VS Shots") 
    goals=team_stat.groupby("Team")["Goals"].sum()
    shots=team_stat.groupby("Team")["Shots"].sum()
    fig6=px.scatter(x=shots,y=goals,color=goals.index, labels={"x": "Shots","y":"Goals","color":"Team"})
    fig6.update_layout(width=1200,height=600,legend_title_text="Team :",xaxis_title_font=dict(size=15,color="white"),yaxis_title_font=dict(size=15,color="white"))
    fig6.update_traces(marker=dict(size=12,line=dict(width=1,color="black")),opacity=0.8)
    st.plotly_chart(fig6,use_container_width=True)
    
   with c4:
    st.subheader("Goals scored VS Shots on target")
    shots_on_target=team_stat.groupby("Team")["Shots on target"].sum()
    fig7=px.scatter(x=shots_on_target,y=goals,color=goals.index, labels={"x": "Shots on target","y":"Goals","color":"Team"})
    fig7.update_layout(width=1200,height=600,legend_title_text="Team :",xaxis_title_font=dict(size=15,color="white"),yaxis_title_font=dict(size=15,color="white"))
    fig7.update_traces(marker=dict(size=12,line=dict(width=1,color="black")))
    st.plotly_chart(fig7,use_container_width=True)

   st.divider()

   st.subheader("Shots VS Shots on target")
   fig8=px.scatter(x=shots,y=shots_on_target,color=goals.index, labels={"x": "Shots","y":"Shots on target","color":"Team"})
   fig8.update_layout(width=1200,height=600,legend_title_text="Team :",xaxis_title_font=dict(size=15,color="white"),yaxis_title_font=dict(size=15,color="white"))
   fig8.update_traces(marker=dict(size=12,line=dict(width=1,color="black")))
   st.plotly_chart(fig8,use_container_width=True)

## Teams dashboard
  with tab2 :
   c5,c6=st.columns(2)
   with c5:
    st.subheader("Top 10 Goal-scoring teams")
    scoring_team=team_stat.groupby("Team")["Goals"].sum().sort_values(ascending=False).head(10)
    fig9=px.bar(x=scoring_team.index,y=scoring_team.values,labels={"x":"Team","y":"Goals"},color_discrete_sequence=["#08a647"],text_auto=True)
    fig9.update_layout(width=1000,height=600,bargap=0.3,xaxis_title_font=dict(size=15,color="white"),yaxis_title_font=dict(size=15,color="white"))
    fig9.update_traces(marker_line_color="black",marker_line_width=1)
    st.plotly_chart(fig9,use_container_width=True)

   with c6:
    st.subheader("Top 8 teams with the highest possession")
    possession_team=team_stat.groupby("Team")["Possession"].mean().sort_values(ascending=False).head(8)
    fig10=px.bar(x=possession_team.index,y=possession_team.values,labels={"x":"Team","y":"Possession (%)"})
    fig10.update_layout(width=1000,height=600,bargap=0.3,xaxis_title_font=dict(size=15,color="white"),yaxis_title_font=dict(size=15,color="white"))
    fig10.update_traces(marker_line_color='black',marker_line_width=1,marker_color="#fcf912")
    st.plotly_chart(fig10,use_container_width=True)

   c7,c8=st.columns(2)
   with c7:
    st.subheader("Top 5 shooting teams")
    shots_team=shots.sort_values(ascending=False).head(5)
    fig11=px.bar(x=shots_team.index,y=shots_team.values,labels={"x":"Team","y":"Shots"},text_auto=True)
    fig11.update_layout(bargap=0.3,width=1000,height=550,showlegend=False,xaxis_title_font=dict(size=15,color="white"),yaxis_title_font=dict(size=15,color="white"))
    fig11.update_traces(marker_line_color='black',marker_line_width=1)
    st.plotly_chart(fig11,use_container_width=True)
   
   with c8:
    st.subheader("Top 5 teams by Shots effinciety")
    goals=team_stat.groupby("Team")["Goals"].sum()
    shots=team_stat.groupby("Team")["Shots"].sum()
    shot_effinciety=goals/shots.replace(0,1)
    eff=shot_effinciety.sort_values().tail(5)
    fig12=px.bar(x=eff.values,y=eff.index,labels={"x":"Shot effinciety","y":"Team"},color_discrete_sequence=["orange"])
    fig12.update_layout(width=1100,height=550,bargap=0.4,xaxis_title_font=dict(size=15,color="white"),yaxis_title_font=dict(size=15,color="white"))
    fig12.update_traces(marker_line_color='black',marker_line_width=1)
    st.plotly_chart(fig12,use_container_width=True)

   st.divider() 

   st.markdown("<h2 style='text-align: center;'>Disciplinary records</h2>",unsafe_allow_html=True)
   st.markdown("   ")

   c9,c10=st.columns(2)
   with c9:
    st.subheader("🟨 Teams with the most yellow cards")
    yellow_cards_team=team_stat.groupby("Team")["Yellow cards"].sum().sort_values(ascending=False).head(10)
    fig13=px.bar(x=yellow_cards_team.index,y=yellow_cards_team.values,labels={"x":"Team","y":"Yellow cards"})
    fig13.update_traces(marker_line_color="black",marker_color="#faf216",marker_line_width=1)
    fig13.update_layout(height=500,xaxis_title_font=dict(size=15,color="white"),yaxis_title_font=dict(size=15,color="white"))
    st.plotly_chart(fig13,use_container_width=True)

   with c10:
    st.subheader("🟥 Teams with the most red cards")
    red_cards_team=team_stat.groupby("Team")["Red cards"].sum().sort_values(ascending=False).head(7)
    fig14=px.bar(x=red_cards_team.index,y=red_cards_team.values,labels={"x":"Team","y":"Red cards"})
    fig14.update_traces(marker_line_color="black",marker_color="#fa1616",marker_line_width=1)
    fig14.update_layout(height=500,title_x=0.5,xaxis_title_font=dict(size=15,color="white"),yaxis_title_font=dict(size=15,color="white")) 
    st.plotly_chart(fig14,use_container_width=True)
   st.subheader("Teams with the most fouls committed") 
   foul_team=team_stat.groupby("Team")["Fouls"].sum().sort_values(ascending=False).head(10)
   fig15=px.bar(x=foul_team.index,y=foul_team.values,labels={"x":"Team","y":"Fouls"})
   fig15.update_layout(width=1000,height=600,bargap=0.3,xaxis_title_font=dict(size=15,color="white"),yaxis_title_font=dict(size=15,color="white"))
   fig15.update_traces(marker_color="#a6fa0a",marker_line_color="black")
   st.plotly_chart(fig15,use_container_width=True)
  
  ## Palyers dashboard
  with tab3:
   st.markdown("<h1 style='text-align: center;'>Players statistics</h1>",unsafe_allow_html=True)
   st.markdown("   ")

   c11,c12,c13=st.columns(3)
   with c11:
    st.subheader("⚽ Top Goals Scorers")
    top_scorers=players.groupby("player")["goals"].sum().sort_values().tail(9)
    fig16=px.bar(x=top_scorers.values,y=top_scorers.index,labels={"x":"Goals","y":"Players"})
    fig16.update_layout(bargap=0.2,height=560,xaxis_title_font=dict(size=15,color="white"),yaxis_title_font=dict(size=15,color="white"))
    fig16.update_traces(marker_line_color="black",marker_line_width=1,marker_color="#16fae7")
    st.plotly_chart(fig16,use_container_width=True)

   with c12:
    st.subheader("🅰️ Players with the most assists")
    top_assist=players.groupby("player")["assists"].sum().sort_values().tail(11)
    fig17=px.bar(x=top_assist.values,y=top_assist.index,labels={"x":"Assists","y":"Players"})
    fig17.update_layout(bargap=0.2,height=560,xaxis_title_font=dict(size=15,color="white"),yaxis_title_font=dict(size=15,color="white"))
    fig17.update_traces(marker_line_color="black",marker_line_width=1,marker_color="#16faae")
    st.plotly_chart(fig17,use_container_width=True)

   with c13:
    st.subheader("Top Contributors (G+A)")
    fig18 = go.Figure()
    players_sorted=players.sort_values(by="Goals + Assists").tail(10)
    fig18.add_bar(y=players_sorted["player"],x=players_sorted["goals"],orientation='h',name='Goals',marker_color="#02C92A")
    fig18.add_bar(y=players_sorted["player"],x=players_sorted["assists"],orientation='h',name='Assists',marker_color="#fa9405")
    fig18.update_layout(xaxis_title="Contributions",yaxis_title="players",bargap=0.3,height=550,xaxis_title_font=dict(size=15,color="white"),yaxis_title_font=dict(size=15,color="white"))
    fig18.update_traces(marker_line_color="black")  
    st.plotly_chart(fig18,use_container_width=True)

   st.subheader("🧤🧤 Top Clean Sheets")
   goal_kepper=players[players["position"]=="Goalkeeper"]
   clean_sheet=goal_kepper.groupby("player")["clean_sheets"].sum().sort_values().tail(7)
   fig19=px.bar(x=clean_sheet.values,y=clean_sheet.index,labels={"x":"Clean Sheets","y":"Players"})
   fig19.update_layout(bargap=0.2,height=560,yaxis_title_font=dict(size=15,color="white"))
   fig19.update_traces(marker_line_color="black",marker_line_width=1,marker_color="#c916fa")
   st.plotly_chart(fig19,use_container_width=True) 

   st.divider()

   st.markdown("<h1 style='text-align: center;'>Player Discipline Overview</h1>",unsafe_allow_html=True)
   
   c14,c15=st.columns(2)
   with c14:
    st.subheader("🟨 Yellow Cards")
    yellow_cards_player=players.groupby("player")["yellow_cards"].sum().sort_values(ascending=False).head(10)
    fig20=px.bar(x=yellow_cards_player.index,y=yellow_cards_player.values,labels={"x":"Player","y":"Yellow cards"})
    fig20.update_layout(bargap=0.2,height=560,xaxis_title_font=dict(size=15),yaxis_title_font=dict(size=15))
    fig20.update_traces(marker_line_color="black",marker_line_width=1,marker_color="#faf216")
    st.plotly_chart(fig20,use_container_width=True)
   
   with c15:
    st.subheader("🟥 Red Cards")
    red_cards_player=players.groupby("player")["red_cards"].sum().sort_values().tail(9)
    fig21=px.bar(x=red_cards_player.index,y=red_cards_player.values,labels={"x":"Player","y":"Red cards"})
    fig21.update_layout(bargap=0.2,height=560,xaxis_title_font=dict(size=15),yaxis_title_font=dict(size=15))
    fig21.update_traces(marker_line_color="black",marker_line_width=1,marker_color="#fa1657")
    st.plotly_chart(fig21,use_container_width=True)

   st.divider() 
   
   #filter players
   st.sidebar.image(r"C:\Users\dell\Desktop\AFCON_Dashboard\Pictures\AFCON_logo.png")
   search = st.sidebar.text_input("🔍 Search a player")
   positions=st.sidebar.multiselect("📍Choose the position of players ",players['position'].unique())
   players_selection=players.query("position in @positions")
   if not positions and not search:
    st.dataframe(players)

   elif search and not positions:
    players_filtered = players[players["player"].str.contains(search, case=False)]
    st.write(players_filtered)

   elif positions and not search:
    st.dataframe(players_selection)
   
   else:
    dff=players_selection[players["player"].str.contains(search, case=False)]
    st.dataframe(dff)

   
   

   
   
    
     

   





 