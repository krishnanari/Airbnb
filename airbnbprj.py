import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import plotly.express as px 
import warnings
warnings.filterwarnings("ignore")
import plotly.graph_objects as go
from plotly.subplots import make_subplots


df = pd.read_csv(r"C:\Users\USER\Downloads\New folder\Airbnb.csv")

# --------------------------------------------------Logo & details on top

#icon = Image.open("airlogo.png")
st.set_page_config(page_title= "Airbnb Analysis | By Dhanalakshmi S",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded")

        #------------------------------------------------------------------HEADER common to all menu
col,coll = st.columns([3,2],gap="small")
#with col:
    #st.image("air.png")
    
    
with coll:
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.markdown("""
                    <style>
                    .centered-text {
                        text-align: center;
                        font-style:italic;
                        font-weight: bold;
                        font-size: 120px; 
                        pointer-events: none;
                    }
                    </style>
                    <div class="centered-text">
                        Analysis
                    </div>
                    """, unsafe_allow_html=True)

    
opt = option_menu(menu_title=None, 
                       options=["Home","Insights","Explore Data","About"],
                icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                #menu_icon="pe.png",
                default_index=0,
                orientation='horizontal',
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#fa5252"},
                        "nav-link-selected": {"background-color": "#fa5252"}})
#------------------------------------HOME
if opt=="Home":

    st.write(" ") 
    st.write(" ")     
    st.markdown("### :red[*OVERVIEW* ]")
    st.markdown("### *This project aims to analyze Airbnb data & perform data cleaning and preparation, develop interactive geospatial visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends in the Airbnb marketplace.*")
    col1,col2=st.columns([3,2],gap="large")
    with col1:
        st.markdown("### :red[*DOMAIN* ] ")
        st.markdown(" ### *Travel Industry, Property Management and Tourism* ")
        st.markdown("""
                    ### :red[*TECHNOLOGIES USED*]    
            
                    ###  *PYTHON*
                    ###  *DATA PREPROCESSING*
                    ### *EDA*
                    ### *PANDAS*
                    ### *VISUALIZATION*
                    ### *STREAMLIT GUI*
                    ### *POWERBI*
                    """)
    with col2:
            st.write(" ")
            st.image("lair.jpg",caption=' ', use_column_width=True)
df1=pd.read_csv("C:/Users/LENOVO/Desktop/Files/Availaibility.csv")

#---------------------------------------- DATA EXPLORATION
if opt=="Explore Data":
    st.write(" ")

    col,col1,col2,col3= st.columns([9,9,9,9],gap="medium")

    with col3:
        on = st.toggle("##### **Geo-spatial visualisation**")
        if on:
               
         #------------------------------------------------------------------How does the availability of listings change based on location?

            df_filtered = df[df['availability_365'] < 365]
            fig = px.scatter_mapbox(df_filtered, lat="latitude", lon="longitude", color="availability_365",
                                    hover_name="suburb", hover_data={"suburb": True, "market": True, "country": True, "availability_365": True},
                                    color_continuous_scale=px.colors.sequential.Viridis,
                                    zoom=1,width=1300,height=700)
            fig.update_layout(mapbox_style="open-street-map", title="Listing Availability by Location")
            st.plotly_chart(fig)
      
            

            #-----------------------------------------------
            st.write("###### **Geospatial Distribution of Listings** ")
            fig = px.scatter_mapbox(df, lat='Latitude', lon='Longitude', color='Price', size='Accomodates',
                                    color_continuous_scale= "Pinkyl",hover_name='Name',range_color=(0,1000), mapbox_style="carto-positron",
                                    zoom=1)
                

            fig.update_traces(hovertemplate='<b>%{hovertext}</b><br><br>Price: %{marker.color}<br>Accommodates: %{marker.size}<br>Country: %{customdata[0]}<br>No. of Reviews: %{customdata[1]}<br>Review Scores: %{customdata[2]}<br>Availability: %{customdata[3]}',
                        customdata=df[['Country', 'No_of_reviews', 'Review_scores','Availability_365']])
            fig.update_layout(width=1250,height=800, title='Geospatial Distribution of Listings')
            fig.update_layout(
            mapbox_style="white-bg",
            mapbox_layers=[
                {
                    "below": 'traces',
                    "sourcetype": "raster",
                    "sourceattribution": "United States Geological Survey",
                    "source": [
                        "https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
                    ]
                }
            ])
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig)

            #------------------------------------------------------------------Are there any spatial clusters of high-priced listings?
            from sklearn.cluster import KMeans         
            df = df.dropna(subset=['Price'])
            X = df[['latitude', 'longitude', 'Price']]
            kmeans = KMeans(n_clusters=5, random_state=42)
            df['cluster'] = kmeans.fit_predict(X)
            fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", color="cluster",
                                    hover_name="suburb", hover_data=["Price"],
                                    color_continuous_scale=px.colors.qualitative.Dark24,
                                    zoom=1,width=1250,height=700)

            fig.update_layout(mapbox_style="open-street-map", title="Spatial Clusters of High-Priced Listings")
            st.plotly_chart(fig)

      
#------------------------------------------------------------------------------------------------------------ Price Analysis  

    with col:
        on = st.toggle("##### **Price Analysis**")

        if on:
            
            st.write(" ")
# How does the average price vary by property type?

            avg_price_by_type = df.groupby("Property_type")["Price"].mean()
            fig = px.line(
                avg_price_by_type.reset_index(),
                x="Property_type",
                y="Price",
                title="Average Price by Property Type in Airbnb Data",width=1300,height=700,
                labels={"Property_type": "Property Type", "Price": "Average Price"},
            )
            fig.update_traces(mode='markers+lines') 
            fig.update_layout(xaxis_title='Property Type', yaxis_title='Average Price')
            st.plotly_chart(fig)

    # Is there a difference in price between superhost and regular host listings?

            Host_is_superhost = df["Host_is_superhost"]
            avg_price_by_host_type = df.groupby(Host_is_superhost)["Price"].mean()
            fig = px.pie(
            avg_price_by_host_type.reset_index(), 
            values="Price",
            names="Host_is_superhost",
            title="Average Price Distribution by Host Type (Superhost vs. Regular)",width=1300,height=700,
            hole=0.5 
        )
            fig.update_traces(textinfo="percent+label", textposition="inside")
            st.plotly_chart(fig)

# How does the price vary across different neighborhoods or cities?
         
            avg_price_by_location = df.groupby("Host_neighbourhood")["Price"].mean()  

            fig = px.bar(
                avg_price_by_location.reset_index(), 
                x="Host_neighbourhood", 
                y="Price",
                color="Host_neighbourhood",width=1410,height=700,
                title="Average Price by Host_neighbourhood (or City)",
                labels={"Host_neighbourhood": "Host_neighbourhood", "Price": "Average Price"},
                 
            )
            st.plotly_chart(fig)

# how review scores influence listing prices the most?
        
            review_scores_prices = df.groupby('Review_scores')['Price'].mean().reset_index()
            review_scores_prices['Price'] = review_scores_prices['Price'].round(3)

            figg = px.scatter(review_scores_prices, x='Review_scores', y='Price', title='Review Scores vs. Average Price',width=1300,height=700,color="Price",color_continuous_scale= "RdBu")
            st.plotly_chart(figg)
            
# How does the price change based on the cancellation policy?
          
            canc_pol= df['Cancellation_policy'].unique()
            fig = make_subplots(rows=1, cols=len(canc_pol), subplot_titles=canc_pol)
            for i, policy in enumerate(canc_pol, start=1):
                data_for_policy = df[df['Cancellation_policy'] == policy]
                fig.add_trace(go.Histogram(x=data_for_policy['Price'], name=policy), row=1, col=i)

            fig.update_layout(title='Distribution of Prices by Cancellation Policy',width=1410,height=700)
            fig.update_xaxes(title_text="Price")
            fig.update_yaxes(title_text="Frequency")
            st.plotly_chart(fig)

#------------------------------------------------------------------------- Avalaibility Analysis

    with col1:
        on = st.toggle("##### **Availability Analysis**")

        if on:
           
            st.write(" " )
 # How does the availability of listings vary by property type?
           
            aaa = df.groupby("Property_type")["availability_365"].mean()
            fig = px.bar(aaa.reset_index(), x="Property_type", y="availability_365", color="availability_365",color_continuous_scale="Rdpu",
                        labels={'x': 'Property Type', 'y': 'Average Availability (Days)'},
                        title='Average Availability by Property Type')
            fig.update_layout(width=1300, height=700)
            fig.update_xaxes(tickangle=45)

            st.plotly_chart(fig)

# What is the overall availability trend of Airbnb listings over time? 

            df1 = df1.drop(columns=['Id'])
            overall_availability = df1.mean()
            overall_availability ['availability_365'] = overall_availability ['availability_365'].round(3)
            fig = px.pie(names=overall_availability.index, values=overall_availability.values,
                        title='Overall Availability Trend of Airbnb Listings',width=1300,height=700,)
            st.plotly_chart(fig)

#---------------------------------------------------------------------------------

# How does the availability of listings change based on the cancellation policy?
           
            avg_data_by_cancellation_policy = df.groupby('Cancellation_policy').agg({'availability_365': 'mean', 'Price': 'mean'}).reset_index()
            avg_data_by_cancellation_policy ['availability_365'] = avg_data_by_cancellation_policy ['availability_365'].round(3)

            fig = px.scatter_3d(avg_data_by_cancellation_policy, x='Cancellation_policy', z='availability_365', y='Price',
                                title='Average Availability and Price by Cancellation Policy',width=1000,height=700,color="availability_365",color_continuous_scale="Plotly3",
                                labels={'Cancellation_policy': 'Cancel Pol', 'availability_365': 'Avg Avail', 'Price': 'Price'})

            st.plotly_chart(fig)

# Is there a relationship between the availability of listings and the number of reviews?

            availability_reviews_df = df[['availability_365', 'No_of_reviews']]
            correlation_matrix = availability_reviews_df.corr()
            fig = px.imshow(correlation_matrix.values,  
                            labels=dict(x='Availability', y='Number of Reviews', color='Correlation'),
                            x=correlation_matrix.columns,
                            y=correlation_matrix.columns,
                            color_continuous_scale='RdBu',
                            title='Correlation Heatmap between Availability and Number of Reviews',width=1300,height=700,)

            st.plotly_chart(fig)

# What is the average availability for different room types?

            avg_availability_by_room_type = df.groupby('Room_type')['availability_365'].mean().reset_index()
            avg_availability_by_room_type ['availability_365'] = avg_availability_by_room_type ['availability_365'].round(3)

            fig = px.pie(avg_availability_by_room_type, values='availability_365', names='Room_type',
                                title='Average Availability by Room Type', hole=0.4,width=1300,height=700,)
            st.plotly_chart(fig)

    
# __________________________________Location Analysis
    with col2:
        on = st.toggle("##### **Location Analysis**")

        if on:
            
 # ---------------------------------------------------------------------  diff countries based on avg review score 
    #-----------------------------------------------------diff countries based on their avg book price

            
            avg_review_score_by_country = df.groupby('Country')['Review_scores_rating'].mean().reset_index()
            avg_review_score_by_country = avg_review_score_by_country.sort_values(by='Review_scores_rating')
            avg_price_by_country = df.groupby('Country')['Price'].mean().reset_index()
            avg_price_by_country = avg_price_by_country.sort_values(by='Price', ascending=False)
            fig = go.Figure()
            fig.add_trace(go.Bar(x=avg_review_score_by_country['Country'], y=avg_review_score_by_country['Review_scores_rating'],
                                name='Average Review Score', marker_color='skyblue'))
            fig.add_trace(go.Bar(x=avg_price_by_country['Country'], y=avg_price_by_country['Price'],
                                name='Average Booking Price', marker_color='lightgreen'))
            fig.update_layout(barmode='group', title='Average Review Score and Booking Price by Country',width=1300,height=700,
                            xaxis_tickangle=-45, xaxis_title='Country', yaxis_title='Value')
            st.plotly_chart(fig)

#-------------------------------------------What are the top amenities offered in listings across different neighborhoods?


            amenities = df['Amenities'].str.replace('[{}]', '', regex=True).str.replace('"', '', regex=True).str.split(',')

            # Count the occurrences of each amenity
            amenity_counts = {}
            for amns in amenities:
                for amenity in amns:
                    amenity = amenity.strip()
                    if amenity in amenity_counts:
                        amenity_counts[amenity] += 1
                    else:
                        amenity_counts[amenity] = 1

            # Sort the amenities by count and select the top N
            sorted_amenities = sorted(amenity_counts.items(), key=lambda x: x[1], reverse=True)
            top_n = 10
            top_amenities = dict(sorted_amenities[:top_n])

            # Create the pie chart
            fig = go.Figure(data=[go.Pie(
                labels=list(top_amenities.keys()), 
                values=list(top_amenities.values()),
                hole=0.4,
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}',
                name=''  
            )])

            fig.update_traces(
                marker=dict(colors=px.colors.qualitative.Pastel)
            )

            fig.update_layout(
                title='Top Amenities Offered in Listings Across Different Neighborhoods',
                width=1300,
                height=700,
              
            )

            # Display the chart using Streamlit
            st.plotly_chart(fig)
            #----------------------------------------Are there any neighborhoods with a significantly higher average review score than others?

            avg_review_score_by_neighborhood = df.groupby('suburb')['Review_scores_rating'].mean().reset_index()
            top_10_neighborhoods = avg_review_score_by_neighborhood.sort_values(by='Review_scores_rating', ascending=False).head(10)
            top_10_neighborhoods['Rank'] = 'Top 10'
            least_10_neighborhoods = avg_review_score_by_neighborhood.sort_values(by='Review_scores_rating', ascending=True).head(10)
            least_10_neighborhoods['Rank'] = 'Least 10'
            merged_neighborhoods = pd.concat([top_10_neighborhoods, least_10_neighborhoods])
            fig = px.bar(merged_neighborhoods, x='suburb', y='Review_scores_rating', color='Rank',
                        labels={'Review_scores_rating': 'Average Review Score'},
                        title='Top and Least 10 Neighborhoods by Average Review Score',width=1200,height=700,
                        color_discrete_sequence=px.colors.qualitative.Pastel)

            fig.update_layout(xaxis_title='Neighborhood', yaxis_title='Average Review Score')
            st.plotly_chart(fig)

#-----------------------------------------------------Are there any differences in the distribution of property types across neighborhoods?

        
            property_type_distribution = df.groupby(['suburb', 'Property_type']).size().reset_index(name='count')

            fig = px.scatter(property_type_distribution, x='suburb', y='count', color='Property_type',
                            title='Distribution of Property Types Across Neighborhoods',width=1110,height=700,
                            labels={'count': 'Number of Listings', 'suburb': 'Neighborhood'})
            fig.update_layout(xaxis_title='Neighborhood', yaxis_title='Number of Listings')
            st.plotly_chart(fig)

        
        

    #---------------------------------------- INSIGHTS
if opt=="Insights":
        st.markdown(
    """
    <style>
        .css-15qegpx {
            display: flex;
            justify-content: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

        analysis_type = st.radio(
             "#### *:red[Choose the Option to Visualize]*",
            ("###### ***:rainbow[Rough Analysis]***", "###### ***:rainbow[Top Charts]***")
        )

     #-----------------------------------------------------------------INSIGHTS 1ST TAB ROUGH ANALYSIS
        if analysis_type == "###### ***:rainbow[Rough Analysis]***":
                dff = pd.read_csv("C:/Users/LENOVO/Desktop/Files/Host.csv")
            
           
                
        #------------------------------------------------------------- ( 1 )
                property_type_counts = df['Property_type'].value_counts()

                fig = px.bar(property_type_counts, x=property_type_counts.index, y=property_type_counts.values,
                            labels={'x': 'Property Type', 'y': 'Count'},
                            title='Distribution of Property Types', width=1300,height=700)

                st.plotly_chart(fig)
                


            #------------------------------------------------------------- ( 2 )
                selected_columns = ['Min_nights', 'Max_nights', 'Accomodates', 'Total_bedrooms', 'Total_beds',
                                'Availability_365', 'Price', 'Security_deposit', 'Cleaning_fee',
                                'Extra_people', 'Guests_included', 'No_of_reviews', 'Review_scores',
                                'Review_scores_accuracy', 'Review_scores_cleanliness',
                                'Review_scores_checkin', 'Review_scores_communication',
                                'Review_scores_location', 'Review_scores_value']

                correlation_matrix = df[selected_columns].corr()
                fig = px.imshow(correlation_matrix,
                                labels=dict(x="Features", y="Features", color="Correlation"),
                                x=selected_columns,
                                y=selected_columns,
                                title='Correlation Heatmap of Airbnb Features',width=1500, height=850)
                for i in range(len(selected_columns)):
                    for j in range(len(selected_columns)):
                        fig.add_annotation(x=selected_columns[i], y=selected_columns[j],
                                        text=str(round(correlation_matrix.iloc[j, i], 2)),
                                        showarrow=False, font=dict(color="black", size=10))
                fig.update_layout(annotations=dict(xref="x", yref="y"))
                st.plotly_chart(fig)

            # -------------------------------------------- ( 3 )

                avg_price_by_capacity = df.groupby('Accomodates')['Price'].mean().reset_index()
                fig = px.bar(avg_price_by_capacity, x='Accomodates', y='Price', 
                        color='Accomodates',width=1300, height=700,
                        labels={'Accomodates': 'Accommodation Capacity', 'Price': 'Average Price'},
                        title='Average Price by Accommodation Capacity',color_continuous_scale= "emrld")
                st.plotly_chart(fig)
            
            #----------------------------------------(4)
                room_type_counts = df['Room_type'].value_counts()
                donut_df = pd.DataFrame({'Room Type': room_type_counts.index, 'Count': room_type_counts.values})
                fig = px.pie(donut_df, values='Count', names='Room Type', hole=0.4)
                fig.update_layout(
                    title='Distribution of Room Types',width=1100, height=700,
                    margin=dict(l=0, r=0, b=0, t=40)
                )
                st.plotly_chart(fig)

            #-------------------------------------------------------------------Which host verification method is the most popular among hosts?
               
                dff['Host_verifications'] = dff['Host_verifications'].fillna('')
                all_verifications = ', '.join(str(verification) for verification in dff['Host_verifications'] if pd.notnull(verification))
                verifications_list = [verification.strip() for verification in all_verifications.split(',')]
                verifications_list = ['Undefined' if verification == '' else verification for verification in verifications_list]
                verification_counts = pd.DataFrame(verifications_list, columns=['Verification Method'])
                verification_counts = verification_counts['Verification Method'].value_counts().reset_index()
                verification_counts.columns = ['Verification Method', 'Count']
                fig = px.bar(
                    verification_counts, 
                    x='Verification Method', 
                    y='Count',
                    title='Popularity of Host Verification Methods',
                    width=1100, 
                    height=700, 
                    color='Verification Method',
                    labels={'Verification Method': 'Host Verification Method', 'Count': 'Number of Hosts'}
                )

                fig.update_layout(
                    xaxis_title='Verification Method', 
                    yaxis_title='Number of Hosts'
                )
                st.plotly_chart(fig)

                
 # ---------------------------------------------------  INSIGHTS 2ND TAB TOP CHARTS

        elif analysis_type =="###### ***:rainbow[Top Charts]***":
                
                title=st.selectbox("Shoot Your Choice",
                                    ["Choose a Title...",
                                     '1.Neighborhoods with the Highest Number of Listings',
                                     '2.Top 10 Most Expensive Neighborhoods',
                                     '3.Number of Available Listings in the Next 30 Days by City',
                                     '4.Top 10 Host IDs with Host Response Times',
                                     '5.Top 10 Countries with the Most Listings',
                                     '6.Top 10 Most Reviewed Listings',
                                     '7.Top 10 Property Types with the Highest Average Review Scores',
                                     '8.Top 10 Most Expensive Property Types by Price',
                                     '9.Top 10 Most Common Amenities Provided in Listings',
                                     '10.Distribution of Average Review Scores for Top Hosts',
                                     '11.Top 10 Most Popular Host Verification Methods'],
                                      index=0)
                
                if title=='1.Neighborhoods with the Highest Number of Listings':

            # Which neighborhoods have the highest number of listings?

                    neighborhood_counts = df['Host_neighbourhood'].value_counts().reset_index()
                    neighborhood_counts.columns = ['Neighborhood', 'Number of Listings']
                    neighborhood_counts = neighborhood_counts.sort_values(by='Number of Listings', ascending=False)

                   
                    fig = px.bar(neighborhood_counts.head(10), x='Neighborhood', y='Number of Listings',
                                labels={'Neighborhood': 'Neighborhood', 'Number of Listings': 'Number of Listings'},
                                title='Neighborhoods with the Highest Number of Listings', width=1300,height=700,color='Number of Listings',color_continuous_scale= "plasma")
                    
                    st.plotly_chart(fig)

                elif title=='2.Top 10 Most Expensive Neighborhoods':

                    # What are the top 10 most expensive neighborhoods in terms of average listing price?

                    avg_price_by_neighborhood = df.groupby('Host_neighbourhood')['Price'].mean().reset_index()
                    avg_price_by_neighborhood = avg_price_by_neighborhood.sort_values(by='Price', ascending=False)
                    top_10_expensive_neighborhoods = avg_price_by_neighborhood.head(10)

                    fig = px.pie(top_10_expensive_neighborhoods, values='Price', names='Host_neighbourhood',
                                title='Top 10 Most Expensive Neighborhoods', width=1300,height=700,
                                hole=0.4)  
                    st.plotly_chart(fig)

                elif title=='3.Number of Available Listings in the Next 30 Days by City':

                    availability_30_by_city = df.groupby('market')['availability_30'].sum().reset_index()
                    availability_30_by_city_sorted = availability_30_by_city.sort_values(by='availability_30', ascending=False)

                    fig = px.bar(availability_30_by_city_sorted, x='market', y='availability_30',color="availability_30",color_continuous_scale='oryel',
                                title='Number of Available Listings for 30 Days over City', width=1300,height=700,
                                labels={'market': 'City', 'availability_30': 'Available'})

                    fig.update_layout(xaxis_title='City', yaxis_title='Available')
                    st.plotly_chart(fig)

                   
                elif title=='4.Top 10 Host IDs with Host Response Times':

                # ---------------------------------What are the top 10 most common host response times?

                    top_host_response_times = df.groupby(['Host_id_y', 'Host_response_time']).size().reset_index(name='Count')
                    top_host_response_times = top_host_response_times.sort_values(by='Count', ascending=False)
                    top_10_host_ids = top_host_response_times['Host_id_y'].head(10)
                    top_10_host_response_times = top_host_response_times[top_host_response_times['Host_id_y'].isin(top_10_host_ids)]
                    fig = px.line(top_10_host_response_times, x='Host_response_time', y='Count', color='Host_id_y', markers=True,
                                labels={'Host_response_time': 'Response Time', 'Count': 'Number of Responses', 'Host_id_y': 'Host ID'},
                                title='Top 10 Host IDs with Host Response Times', width=1300,height=700)

                    st.plotly_chart(fig)

                elif title=='5.Top 10 Countries with the Most Listings':

                    # What are the top 10 countries with the most listings? 

                    listings_by_country = df['Country'].value_counts().reset_index()
                    listings_by_country.columns = ['Country', 'Number of Listings']
                    listings_by_country = listings_by_country.sort_values(by='Number of Listings', ascending=False)
                    top_10_countries = listings_by_country.head(10)

                    fig = px.bar(top_10_countries, x='Number of Listings', y='Country', orientation='h',
                                labels={'Number of Listings': 'Number of Listings', 'Country': 'Country'},
                                title='Top 10 Countries with the Most Listings', width=1300,height=700,color='Number of Listings',color_continuous_scale='Purpor')

                    st.plotly_chart(fig)

                elif title=='6.Top 10 Most Reviewed Listings':

                    #--------------------------What are the top 10 most reviewed listings?

                    top_10_most_reviewed_listings = df.nlargest(10, 'No_of_reviews')
                    fig = px.scatter(top_10_most_reviewed_listings, x='Id', y='No_of_reviews',
                                    labels={'Id': 'Listing ID', 'No_of_reviews': 'Number of Reviews'},
                                    title='Top 10 Most Reviewed Listings', width=1300,height=700,color='No_of_reviews',color_continuous_scale='Aggrnyl')
                    st.plotly_chart(fig)

                elif title=='7.Top 10 Property Types with the Highest Average Review Scores':

                  #---------------------What are the top 10 property types with the highest average review scores? 

                    avg_review_scores_by_property_type = df.groupby('Property_type')['Review_scores_rating'].mean().reset_index()
                    avg_review_scores_by_property_type = avg_review_scores_by_property_type.sort_values(by='Review_scores_rating', ascending=False)
                    top_10_property_types = avg_review_scores_by_property_type.head(10)
                    fig = px.line(top_10_property_types, x='Property_type', y='Review_scores_rating', markers=True,
                                labels={'Property_type': 'Property Type', 'Review_scores_rating': 'Average Review Scores'},
                                title='Top 10 Property Types with the Highest Average Review Scores', width=1300,height=700)

                    st.plotly_chart(fig)

                elif title=='8.Top 10 Most Expensive Property Types by Price':

                # --------------------------------What are the top 10 most expensive property types by price ? 

                        avg_price_by_property_type = df.groupby('Property_type')['Price'].mean().reset_index()
                        avg_price_by_property_type['Price'] = avg_price_by_property_type['Price'].round(3)
                        top_10_expensive_property_types = avg_price_by_property_type.sort_values(by='Price', ascending=False).head(10)
                        fig = px.bar(top_10_expensive_property_types, x='Property_type', y='Price',color="Price",color_continuous_scale='Pinkyl',
                                    title='Top 10 Most Expensive Property Types by Price', width=1300,height=700,
                                    labels={'Property_type': 'Property Type', 'Price': 'Average Price'})
                        st.plotly_chart(fig)

                        top_10_expensive_property_types = avg_price_by_property_type.sort_values(by='Price', ascending=False).head(10)
                        fig = px.bar(top_10_expensive_property_types, x='Property_type', y='Price',color="Price",color_continuous_scale='Pinkyl',
                                    title='Top 10 Most Expensive Property Types by Price', width=1300,height=700,
                                    labels={'Property_type': 'Property Type', 'Price': 'Average Price'})
                        st.plotly_chart(fig)

                elif title=='9.Top 10 Most Common Amenities Provided in Listings':

                #----------------------------------------What are the top 10 most common amenities provided in listings?

                    all_amenities = ', '.join(df['Amenities'])
                    amenities_list = [amenity.strip() for amenity in all_amenities.split(',')]
                    amenity_counts = pd.Series(amenities_list).value_counts().reset_index()
                    amenity_counts.columns = ['Amenity', 'Count']

                    top_10_common_amenities = amenity_counts.head(10)

                    fig = px.pie(top_10_common_amenities, values='Count', names='Amenity',
                                title='Top 10 Most Common Amenities Provided in Listings', width=1300,height=700)
                    st.plotly_chart(fig)

                # ------------------------------------ Which city has the highest number of available listings in the next 30 days?

                elif title=='10.Distribution of Average Review Scores for Top Hosts':

                   
                    avg_review_scores_by_host = df.groupby('Host_id_y')['Review_scores_rating'].mean().reset_index()
                    avg_review_scores_by_host = avg_review_scores_by_host.sort_values(by='Review_scores_rating', ascending=False)
                    top_hosts = avg_review_scores_by_host.head(10)

                    fig = px.pie(top_hosts, values='Review_scores_rating', names='Host_id_y',
                                title='Distribution of Average Review Scores for Top Hosts', width=1300,height=700,color='Host_id_y',
                                hole=0.4)  
                    st.plotly_chart(fig)

                elif title=="11.Top 10 Most Popular Host Verification Methods":
                    dff = pd.read_csv("C:/Users/LENOVO/Desktop/Files/Host.csv")

                #-----------------------------------------Which host verification method is the most popular among hosts?

                    
                    df['Host_verifications'] = dff['Host_verifications'].astype(str)
                    all_verifications = ', '.join(df['Host_verifications'])
                    verifications_list = [verification.strip() for verification in all_verifications.split(',')]
                    verification_counts = pd.Series(verifications_list).value_counts().reset_index()
                    verification_counts.columns = ['Verification Method', 'Count']
                    top_10_verification_methods = verification_counts.sort_values(by='Count', ascending=False).head(10)
                    fig = px.bar(top_10_verification_methods, x='Verification Method', y='Count', color="Count", 
                                color_continuous_scale='bluyl',
                                title='Top 10 Most Popular Host Verification Methods', width=1300, height=700,
                                labels={'Verification Method': 'Host Verification Method', 'Count': 'Number of Hosts'})

                    fig.update_layout(xaxis_title='Verification Method', yaxis_title='Number of Hosts')
                    st.plotly_chart(fig)
                                

if opt=="About":
    st.markdown("### :red[*AIRBNB* ] ")
    st.write(' ### *Airbnb is an online marketplace that connects people who want to rent out their property with people who are looking for accommodations,typically for short stays. Airbnb offers hosts a relatively easy way to earn some income from their property.Guests often find that Airbnb rentals are cheaper and homier than hotels.* ')
    st.write("")
    st.write(' ### *Airbnb Inc (Airbnb) operates an online platform for hospitality services.The company provides a mobile application (app) that enables users to list,discover, and book unique accommodations across the world.The app allows hosts to list their properties for lease, and enables guests to rent or lease on a short-term basis,which includes vacation rentals, apartment rentals, homestays, castles,tree houses and hotel rooms.* ')
    st.write(' ### *The company has presence in China, India, Japan, Australia, Canada, Austria, Germany, Switzerland, Belgium, Denmark, France, Italy, Norway, Portugal, Russia, Spain, Sweden, the UK, and others.Airbnb is headquartered in San Francisco, California, the US.* ')
    
   
    st.markdown("### :red[*BACKGROUND OF AIRBNB* ] ")
    st.write(' ### *Airbnb was born in 2007 when two Hosts welcomed three guests to their San Francisco home, and has since grown to over 4 million Hosts who have welcomed over 1.5 billion guest arrivals in almost every country across the globe.* ')
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    col11,col22=st.columns([2,3],gap="small")
    with col11:
         st.write(" ")
    with col22:
         
      st.image("airr.png")

    st.markdown(
    """
    <div style="display: flex; justify-content: center;">
        <a href="https://github.com/Dhanalakshmi177/Capstone-Project-4" style="color: violet; font-weight: bold; text-decoration: none; padding: 10px 20px; background-color: white; border: 2px solid violet; border-radius: 5px;">GitHub</a>
    </div>
    """,
    unsafe_allow_html=True
)
























