# This is the image conversion package <image_conversion>

**clone the package into your <your_workspace>/src/**  
```bash
cd <your_workspace>/src
```
```bash
git clone  https://github.com/abhiDharwad/image_convertion_task.git
```
```bash
cd ~/<your_workspace>
```
```bash
rosdep install --from-paths src -y --ignore-src
```

**build the package **
```bash
colon build --symlink-install
```
**open two terminal and source them**
```bash
source /opt/ros/humble/setup.bash
```
```bash
source ~/<your_workspace>/install/setup.bash
```
**In first window run the service server**
```bash
ros2 launch image_conversion cameraConverter.launch  
```
**In second window run the service client**
```bash
ros2 run image_conversion client <gray>true <color>false 
```   

![alt text](<image_conversion/png/Screenshot from 2025-11-12 00-07-28.png>)


![alt text](<image_conversion/png/Screenshot from 2025-11-12 00-07-02.png>)