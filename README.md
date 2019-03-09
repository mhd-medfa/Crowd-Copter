# Crowd-Copter

![Crowd Management System](./images/Crowd%20Management.png)


Crowds of people formed due to either a civil event or an emergency are one of the most vulnerable places which lead to enormous numbers of injuries and deaths among human souls.

The goal of this project is to reduce those regrettable numbers of deaths and injuries by developing a system that consists of a camera fixed on Autonomous Navigatation Flying Robot to capture the scene, which connected to the Raspberry Pi 3 Model B Kit to analyze the captured scenes on the real time. We will be able to guide the people to continue their movement through the right and safe direction without impact or collision.

Our system keeps track of moving keypoints to detect the coherent motion patterns in the scene.
In our project, we implement a Coherent Neighbor Invariance, which characterizes the local spatiotemporal relationships of individuals in coherent motion. This Algorithm can work efficiently on scenes for mobile objects (people, cars, bicycles, animals, ..etc), which gives Coherent Filter many applications in different fields.

![Flowchart](./images/Flowchart.jpeg)

However, in this project, the experiments will be concentrated on people motions in crowded places. The figure below shows how Crowd Copter aims to analyz the people motions in the input scene and classified them into different clusters each of them has a unique color.

![Input vs Output](./images/fianlResult.png)
