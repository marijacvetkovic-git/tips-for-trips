# tips_for_trips

## Technologies:
- Flask framework (Python 3.9.0)
- ReactJS with ANT Design
## Starting the app
### `flask run`
### `npm start`

## Before registration

Recommendation system using K-Means clustering and relationships between enitites to recommend destinations (attractions) to user. A Memgraph databased is used in this application because of advantages of graph databases (speed and easy menage realtionships). 

When the application starts, it displays destinations that are most recommended to users. Here, there is no personalized recommendation because the user is not logged in yet.
Images 1 and 2 depict the homepage when the user is not logged in, and in image 3, the recommendation function for non-logged-in users is shown.

![image](https://github.com/marijacvetkovic-git/tips-for-trips/assets/101969164/bf2c68fb-9393-4d7f-89eb-caf295d7fb1c)
![image](https://github.com/marijacvetkovic-git/tips-for-trips/assets/101969164/02981a45-516b-4bbd-986c-6dd877cb65ba)
![image](https://github.com/marijacvetkovic-git/tips-for-trips/assets/101969164/7ee779b2-71c8-4026-9ed4-3abcaacb9388)

When the user is not logged in, they can open a card about a specific attraction. It includes the title, images of the attraction, 
average rating, description of the attraction itself, and activities offered by that attraction. At the bottom of the page, there are hashtags describing the attraction.

![image](https://github.com/marijacvetkovic-git/tips-for-trips/assets/101969164/029cc33b-1df6-4f68-b2b2-38213803f8ca)
![image](https://github.com/marijacvetkovic-git/tips-for-trips/assets/101969164/c8992db5-1f3f-44bc-9647-dd8b075df0d1)
![image](https://github.com/marijacvetkovic-git/tips-for-trips/assets/101969164/6192f7e4-a282-43fc-9d31-0513d8bf8d3c)

When you click on one of the offered activities, basic information about it is provided: approximate duration of the activity, 
whether any prior experience is required, and the age range of participants allowed to participate.

![image](https://github.com/marijacvetkovic-git/tips-for-trips/assets/101969164/ace3e7cd-962e-48de-a39a-95d2142cee1f)

In addition to being able to browse specific attractions, the user can also search for them. Firstly, if the name of a city is entered, it returns attractions offered by that city.
Otherwise, a search is conducted by name, i.e., whether the attraction starts with or contains the entered text as its name.

![image](https://github.com/marijacvetkovic-git/tips-for-trips/assets/101969164/4eda1f86-a846-4692-a8a9-f1859431a9a6)
![image](https://github.com/marijacvetkovic-git/tips-for-trips/assets/101969164/0efccd2a-436f-4a70-9b98-a444ef3e4445)

## Registration
When the user wants to register, they will select the "Register/LogIn" option from the menu bar. Upon clicking, a registration form will open, where the user needs to enter basic information such as username, password, date of birth, and everything else listed in the form. If a user already exists with that username, or if the given email already exists, or if an invalid date is selected, an error will be displayed to the user which they can correct.

![image](https://github.com/marijacvetkovic-git/tips-for-trips/assets/101969164/87b86aa3-8f82-4ecd-a97b-ac386b606acf)

When the "Ok" button is clicked, a form appears to find out what the user likes to see.
This form is used to create a "WANTS_TO_SEE" link, which is used in creating recommendations when the user is new to the site. At least three options need to be selected to proceed further.

![image](https://github.com/marijacvetkovic-git/tips-for-trips/assets/101969164/d5ad6264-4e67-4743-9d56-79ed5ceeec5d)

## Log in
When the user successfully registers, they can log in to the site. They enter the username and password required to log in. 
If both pieces of information are correct, they can log in.

![image](https://github.com/marijacvetkovic-git/tips-for-trips/assets/101969164/14d26ea8-04f8-43f1-893c-3900f1264ed6)

## Recommendations obtained through the "WANTS_TO_SEE" link

Since the new user hasn't marked anything as visited, attractions obtained through the "WANTS_TO_SEE" link are displayed to them.
![image](https://github.com/marijacvetkovic-git/tips-for-trips/assets/101969164/299bbe83-e5cb-4846-bd36-430938833bbb)

During registration, the hashtags "Nature", "History", and "Park" were selected, and these destinations offer them as well. Below are listed attractions and hashtags describing them:

QueensTown: "Restaurant", "Park", "Canyon"
Mount Everest: "Nature", "Discover Earth", "Journey of Discovery", "Nature Escape"
Angkor Wat: "History", "Discover Earth", "Historic Sites", "Journey of Discovery", "Nature", "Landmarks", "Sightseeing", "Cultural Heritage", "Travel Dreams", "Must-See Places"
Vatican Museums: "History", "Discover Earth", "Historic Sites", "Journey of Discovery", "Landmarks", "Sightseeing", "Cultural Heritage"
Al-Khazneh: "Nature", "Historic Sites", "Landmarks", "Sightseeing", "Cultural Heritage", "Travel Dreams", "Must-See Places", 
"Global Tourism", "Adventure Awaits", "Journey of Discovery"
Regarding filtering based on the "WANTS_TO_SEE" link, it was mentioned that during registration, a simpler version of the 
filtering script is initiated. This function returns attractions that have certain hashtags and only considers the average rating of that attraction. 
It exists because it's possible for the user to log in for the first time before the script is run.When the script is executed and the user hasn't 
visited anything yet, the recommendations will appear as shown in the image.

![image](https://github.com/marijacvetkovic-git/tips-for-trips/assets/101969164/78f80bcc-bfdc-4ec5-8e28-e6586b68f860)

This makes sense because "Angkor Wat" contains 2 out of the 3 hashtags the user specified and has a good rating. The others are also highly rated and have 1 matching hashtag.
 ## Recommendations obtained through K-means clustering
 The functionality of the K-means algorithm has been verified using an example of a user visiting the "Acropolis" attraction, which they rated as 5.
 
 ![image](https://github.com/marijacvetkovic-git/tips-for-trips/assets/101969164/a510be94-3090-4ef3-87e3-870ebf29ce6b)
 ![image](https://github.com/marijacvetkovic-git/tips-for-trips/assets/101969164/f87eedac-60bc-4130-82f7-f01120d08fe3)

 The "Acropolis" attraction has the hashtags: "History", "Discover Earth", "Historic Sites", "Journey of Discovery", "Landmarks", "Sightseeing", "Cultural Heritage". The clustering script has been executed. Since only one attraction has been visited, recommendations can be made from only one cluster. In this specific case, "Acropolis" belongs to cluster 2, which has 5 elements including it. This means there are only 4 attractions that can be recommended based on this criterion. In this case, we take the hashtags from the "WANTS_TO_SEE" link and consider attractions that have those hashtags. So, we obtained 4 attractions through the K-means algorithm and one through the "WANTS_TO_SEE" link.

 ![image](https://github.com/marijacvetkovic-git/tips-for-trips/assets/101969164/9154219c-f54b-4235-8f35-ff68da5b1eea)

 "Acropolis" has the hashtags: "History", "Discover Earth", "Historic Sites", "Journey of Discovery", "Landmarks", "Sightseeing", "Cultural Heritage". Attractions from the same cluster are:

Stonehenge ("Landmarks", "Historic Sites", "History", "Cultural Heritage", "Adventure Awaits", "Journey of Discovery")
Vatican Museums ("History", "Discover Earth", "Historic Sites", "Journey of Discovery", "Landmarks", "Sightseeing", "Cultural Heritage")
Machu Picchu ("History", "Discover Earth", "Historic Sites", "Journey of Discovery")
Angkor Wat ("History", "Discover Earth", "Historic Sites", "Journey of Discovery", "Nature", "Landmarks", "Sightseeing", "Cultural Heritage", "Travel Dreams", "Must-See Places").
Observing the hashtags of these attractions, it makes sense why they are in the same cluster. Each of them has hashtags: "History", "Historic Sites", "Journey of Discovery", while "Discover Earth", "Landmarks", and "Cultural Heritage" appear in 3 attractions, and "Sightseeing" in two. In this regard, clustering has shown to be effective.

If the user visits another attraction, for example, "Čegar", which has the hashtags "History" and "Museum", the "VISITED" link is created with two attractions from clusters 2 and 1. Since "Čegar" has been rated highly and was recently added, attractions from its cluster will be recommended first. If there are fewer than 5 attractions in its cluster, we move to cluster 2. However, in cluster 1, there are more than 5 elements that can be recommended, so there's no need for attractions from cluster 2.

![image](https://github.com/marijacvetkovic-git/tips-for-trips/assets/101969164/11903e94-73d8-4e38-970a-6bafd98b7f93)

Does it make sense for these attractions to be in the same cluster? Cerjan Cave: "Nature", "Museum", "History", "Cave" Neuschwanstein Castle: "Castle",
"History", "Cultural Heritage", "Historic Sites" Kalemegdan: "Monument", "History" The Skull Tower: "Museum", "History" Mesa Verde National Park: "Museum", "History", "Canyon" Considering the hashtags of these attractions, it makes sense why they are in the same cluster. Most hashtags appear in each of the attractions, so the system works well. 
What happens if attractions are only chosen from the same cluster? Suppose the user has not visited "Čegar", but "Stonehenge", which is from the same cluster as the previously visited "Acropolis". Then the hashtags from the "WANTS_TO_SEE" link are used to create recommendations more than before. If the user visits all attractions from one cluster, the recommendation system from the beginning is used, i.e., only with the "WANTS_TO_SEE" link. This is one of the weaknesses of this system.


## "Near You" Recommendations
If the user wants to see attractions in their vicinity, they can simply click on the blue button with the location icon. This is enabled because the system captures the user's location upon each login, and then, by clicking the button, queries are made to retrieve the nearest attractions. For example, if we are currently near "The Skull Of Tower", the attractions that the system identifies as nearby are those shown in the image.

 ![image](https://github.com/marijacvetkovic-git/tips-for-trips/assets/101969164/58971557-2977-49d9-8654-3f4d85d17a19)

 These recommendations make sense because only attractions within Niš and Belgrade are displayed. When creating "Near You" recommendations, the distance between two locations is used. The distance between two points on Earth can be calculated using the Haversine formula, which relies on trigonometric functions. 

 
## Other functionalities of the application

Although the main goal of this work is to design a recommendation system, the application itself has other functionalities. When the user is logged in to the site, in addition to being shown recommendations, they also have the option to plan a trip to a specific city. This functionality is initiated by clicking on the "Plan trip" option on the menu bar, and a form like the one shown in the image opens.

![image](https://github.com/marijacvetkovic-git/tips-for-trips/assets/101969164/4c7932fe-e891-4843-85c6-ee176dd80a97)

The user needs to specify the city they want to travel to. They also have the option to choose how far attractions should be from their current location. For example, if the user is on vacation and decides to go on a short tour but doesn't know what to visit. Additionally, they can select some activities that attractions should ideally offer. The duration of the tour along with these activities is another option the user can add. If it's important to the user that attractions have parking or are "family-friendly," they can choose that option as well.

![image](https://github.com/marijacvetkovic-git/tips-for-trips/assets/101969164/c7e09b81-dfc2-4de1-a7d5-a899ec453204)


Also, the logged-in user has the option to search for attractions in various ways. It's possible to search for attractions by city, activities, or hashtags, as seen in the image.
![image](https://github.com/marijacvetkovic-git/tips-for-trips/assets/101969164/d9d7bc8f-0a3c-4272-80b6-d7987aa8f0dd)

During the search, information about the user is taken into account. When using the search tag "all," in addition to comparing the entered text with the city name, attraction name, and description, the hashtags that the user expressed interest in are also considered. It's possible to perform a search with the "city" tag where attractions located in a city whose name matches the entered text are considered. If any of these attractions have hashtags that the user expressed interest in, they will be prioritized in the results.

![image](https://github.com/marijacvetkovic-git/tips-for-trips/assets/101969164/1034d4cb-ced5-43cb-b2b4-81d95705e7e4)


During the search marked as "attraction," the system checks if the attraction's name contains the specified text. Then, it considers how many of its hashtags match the hashtags the user expressed interest in. Additionally, it checks if the attraction's description contains the specified text.

![image](https://github.com/marijacvetkovic-git/tips-for-trips/assets/101969164/d532b2e5-b82e-4d7d-b785-4ecf01c39df7)


If the search is performed with the tag "hashtag," the system looks at which attractions have that hashtag. Then, it considers how many hashtags match the user's preferences, followed by the rating of the attraction itself.

![image](https://github.com/marijacvetkovic-git/tips-for-trips/assets/101969164/e493af00-33bb-475c-8512-6c8525baaf46)
![image](https://github.com/marijacvetkovic-git/tips-for-trips/assets/101969164/06d31639-aec1-4ebd-935a-446444f4d94b)


In the search labeled "activity," the system looks at which attractions have the activities entered in the search field. In addition to regular users, there is also an admin. An admin is a user who, in addition to the regular functionalities available to users, can add and delete attractions, cities, activities, and hashtags. Additionally, they have the ability to create and delete links between certain entities.








 














