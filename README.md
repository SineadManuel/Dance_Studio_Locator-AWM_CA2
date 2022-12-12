# AWM CA2

The purpose of this assignment was to create a location-based services application which contains the following technologies:
- Database: PostgreSQL with PostGIS
- Middle tier(s): Django with Django REST Framework
- Front-end: Progressive Web Application (PWA) and Android or iOS app developed in Cordova. You can use any framework you like for layout such as jQueryMobile, Ionic, Bootstrap etc.
- Mapping: Leaflet JS with OpenStreetMap
- Deployment (middle tier(s)): Any cloud provider. I suggest using Docker to create an image and deploy an instance of this. The back-end components of your app must be web-accessible or the front-end component will not work.

The plan for my project was to locate dance studios that are around the user's location. Unfortunately, I was not able to actually make this functionality work.

Currently, my application can:
- Register a user
- Login a user
- Display a map containing the user's location
- Logout a user
- Option to download PWA

I have attempted to locate dance studios around the user's area but ultimately could not fully get this functionality working. You can see my attempts in the find_studio method in views.py and the findStudio method maps.html.

I did manage to create my web app into a PWA. Below shows two pictures: first picture shows the option of downloading the PWA, second picture shows the PWA in use

### Installation of PWA
![Screenshot (10)](https://user-images.githubusercontent.com/71662080/206944752-bba918b3-0f95-42fa-807a-467345b2a5c4.png)


### PWA Fullscreen

![Screenshot (12)](https://user-images.githubusercontent.com/71662080/206945163-c43214f4-1754-47b8-8970-f2a8747c9f4d.png)


Unfortunatly, I was also unable to deloy my web app due to converting my app into a PWA.

I noticed that PWA only works with Django 3, however my Django version is 4.1.4.
To get PWA to work I had to manually modify a urls.py file within the in a pwa directory which was in the site-packages. Although I can download a PWA, that has now caused a problem with creating my app contain for docker. A picture of the error is below. This is the same error I got before I modified urls.py
<img width="728" alt="image" src="https://user-images.githubusercontent.com/71662080/206954231-bc3b45a8-6159-4c9f-8949-3941c4fb81fc.png">

My domain is activated, however it only displays NGINX.
Link to domain: https://sineadmanuel.online/

### sineadmanuel.online
![image](https://user-images.githubusercontent.com/71662080/206954373-1f5d62b9-8a69-4845-9003-864c0db98983.png)

