import streamlit as st
import pandas as pd
import pickle

# Load the data
popular = pickle.load(open('popular.pkl', 'rb'))

# Streamlit app configuration
st.set_page_config(page_title="Popular Book Recommendations", layout="wide")

# Title and Description
st.title("📚 Popular Book Recommendations")
st.write("""
This application showcases the most popular books based on the number of ratings and average ratings. 
Explore the top books, their authors, and ratings.
""")

# Sidebar for user navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Select an option:", ["Home", "Recommendations"])

# Home Page
if options == "Home":
    st.header("Top Recommended Books")

    # Display the DataFrame
    st.write("Below is the list of top 50 popular books:")
    for i in range(len(popular)):
        st.subheader(f"**{popular.iloc[i]['Book-Title']}**")
        st.write(f"**Author**: {popular.iloc[i]['Book-Author']}")
        st.write(f"**Average Rating**: {popular.iloc[i]['avg_rating']}")
        st.write(f"**Number of Ratings**: {popular.iloc[i]['num_ratings']}")
        st.image(popular.iloc[i]['Image-URL-M'], width=150)
        st.markdown("---")

# Recommendations Page
if options == "Recommendations":
    st.header("📖 Get Recommendations for a Book")
    
    # Input from user
    book_name = st.text_input("Enter the name of a book you like:", "")
    
    # Function to get recommendations
    def recommend(book_name):
        from sklearn.metrics.pairwise import cosine_similarity
        import numpy as np

        # Load additional data for collaborative filtering
        pt = pickle.load(open('pt.pkl', 'rb'))  # Pivot table
        similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))  # Precomputed similarity
        
        try:
            # Index fetch
            index = np.where(pt.index == book_name)[0][0]
            similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:5]
            
            data = []
            for i in similar_items:
                item = []
                temp_df = popular[popular['Book-Title'] == pt.index[i[0]]]
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
                data.append(item)
            return data
        except:
            return []
    
    # Display recommendations
    if st.button("Get Recommendations"):
        if book_name:
            recommendations = recommend(book_name)
            if recommendations:
                st.subheader("Books similar to your choice:")
                for rec in recommendations:
                    st.write(f"**Title**: {rec[0]}")
                    st.write(f"**Author**: {rec[1]}")
                    st.image(rec[2], width=150)
                    st.markdown("---")
            else:
                st.error("No recommendations found. Try a different book name.")
        else:
            st.error("Please enter a book name.")

# Footer
st.sidebar.markdown("---")
st.sidebar.write("Developed with ❤️ using Streamlit")
