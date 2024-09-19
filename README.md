# SpeedcamST

A do-it-yourself speed camera.

This project will require the following skills:
- Linux
- Minor electronics
- Python
- Craftiness 

<img src="https://github.com/user-attachments/assets/5c8aa0a5-a9bc-4123-b99a-581fedbf7416" width=10.4% height=10.4%>
<img src="https://github.com/user-attachments/assets/f231b58b-27e5-4d49-8015-25b948db93ea" width=7.5% height=7.5%>
<img src="https://github.com/user-attachments/assets/9ccf3dde-4ece-4f20-99ab-77cc4d141fc6" width=7.5% height=7.5%>
<img src="https://github.com/user-attachments/assets/17bfb688-7fd2-44aa-aca3-9f660bfaa98c" width=11.5% height=11.5%>
<img src="https://github.com/user-attachments/assets/c1035574-3ada-4074-8468-6e33d227e2a8" width=7.5% height=7.5%>
<img src="https://github.com/user-attachments/assets/52cdacab-25e5-467e-a9a7-47215db879b3" width=7.5% height=7.5%>
<img src="https://github.com/user-attachments/assets/9527d8b8-f94d-42f0-adea-028677bc60cf" width=7.5% height=7.5%>
<img src="https://github.com/user-attachments/assets/a13dfff8-6c75-4a6e-baf9-7db6f7b3836c" width=20% height=20%>

## Hardware

I am using a Raspberry Pi 4, but I recommend getting a 5. It should handle the object detection far better. It takes some time for the 4 to process the video. 

The adapters are used to mount the camera to the door of the enclosure. The lens I chose does not have any threads on it. I modified the 27mm-30mm adapter by filing off the outer threads. This allowed it to fit inside the ring of the lens. I used super glue gel to attach it. 

For the outside step adapter, I used paintable silicone to attach it to the enclosure along with the camera shroud, fans, and round vents. The camera shroud will need some modification for the step up adapter to fit inside of it.

I purchased the C version of the radar because I thought I would be using the range function. I wound up not using it and have recommended the A version. Be sure to read the documentation they provide on their website. To calibrate the radar, I used the cosine correction and made passes with my car with the corrections in the config file set to 0. Since my car has a digital speedometer, it really made it easy. Based on local roadside police radars, my speedometer read 1 mph faster. Any discrepancies between the radar report and my speedometer were entered into the config file.

Raspberry Pi 4 or 5, 8GB RAM</br>
[Omni Presense OPS243-A](https://omnipresense.com/product/ops243-doppler-radar-sensor/)</br>
[Pi heatsink and fan](https://www.amazon.com/gp/product/B07Z3Q417K/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)</br>
[Pi SSD mount](https://www.amazon.com/gp/product/B09MLP4NBM/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)</br>
[Enclosure](https://www.amazon.com/gp/product/B08281V2RL/ref=ppx_yo_dt_b_asin_title_o05_s00?ie=UTF8&psc=1)</br>
[50mm fans](https://www.amazon.com/gp/product/B00N1Y3XP6/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)</br>
[Round vents](https://www.amazon.com/dp/B089211YPJ/?coliid=I23TO4LJPV9P0H&colid=2QKYPFE10UPBM&psc=1&ref_=list_c_wl_lv_ov_lig_dp_it)</br>
[Outside step up adapter (25mm-58mm)](https://www.amazon.com/gp/product/B0899BYLHD/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)</br>
[Clear lens filter](https://www.amazon.com/gp/product/B000A84H4C/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1)</br>
[Stepdown adapter (30mm-35mm)](https://www.amazon.com/gp/product/B089Q13T22/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)</br>
[Step up adapter (27mm-30mm)](https://www.amazon.com/gp/product/B0899WW7ZY/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)</br>
[Camera shroud](https://www.amazon.com/gp/product/B0BP6KW7V8/ref=ppx_yo_dt_b_asin_title_o04_s00?ie=UTF8&psc=1)</br>
[HQ camera](https://www.amazon.com/gp/product/B09YHN5DBY/ref=ppx_yo_dt_b_asin_title_o09_s00?ie=UTF8&psc=1)</br>
[Enclosure mount](https://www.amazon.com/gp/product/B07KT13216/ref=ppx_yo_dt_b_asin_title_o03_s00?ie=UTF8&psc=1)</br>
[POE Injector](https://www.amazon.com/gp/product/B09SXSN3XT/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)</br>
[POE surge protector](https://www.amazon.com/gp/product/B07X27RXSL/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)</br>
[POE Splitter](https://www.amazon.com/gp/product/B087F4QCTR/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)</br>
[Temperature sensor](https://www.amazon.com/gp/product/B0BQVQXB7T/ref=ppx_yo_dt_b_asin_title_o06_s00?ie=UTF8&psc=1)</br>
[Cable clips for temperature sensor](https://www.amazon.com/gp/product/B0CGRXNLWF/ref=ppx_yo_dt_b_asin_title_o04_s00?ie=UTF8&psc=1)</br>
[USB connector for 5v power](https://www.amazon.com/gp/product/B0BV9K69M9/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&th=1)</br>
[Dupont terminal block](https://www.amazon.com/gp/product/B08G1D97YY/ref=ppx_yo_dt_b_asin_title_o03_s00?ie=UTF8&psc=1)</br>
[Relay](https://www.amazon.com/HiLetgo-Channel-optocoupler-Support-Trigger/dp/B00LW15A4W/ref=sr_1_3?crid=32DAI98P02I2A&dib=eyJ2IjoiMSJ9.iefdivWxoOd9fm9I4CKg6OdfLdUfbNrts67g-QP3r-JBZVGd6PQj8V4_ffqp0gcGsOEPPP5RbHR65ae14G4B6xvMqafRNljP1HMb5cyUbv-3t_Cfo1vGM4wjiAOWDQ13kq865kdH2dW0clssJjqsPdWWLaOSUS-KkIFM3616YkODa5fDkoqhXMXR3Ha4alJwD593tbdjm7akoP_CEe-l-Vthu_dZMQL4xvi85_dIzDMlODC8dUTKKCSFrlvrO5yTg0rIY-nSLLGeHWLLnqLEIQEpliyKtbiS1VakDl3GH7Y.4wGlSOJ2fhlhvTfj_KDSkPuHIDtS9gaBri0G5NJ6vkM&dib_tag=se&keywords=arduino+relay&qid=1724533558&s=industrial&sprefix=arduino+relay%2Cindustrial%2C77&sr=1-3)</br>
[Waterproof ethernet connector](https://www.amazon.com/gp/product/B07PH4GL2F/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1)</br>
[Standoffs](https://www.amazon.com/gp/product/B01N5RDAUX/ref=ppx_yo_dt_b_asin_title_o05_s01?ie=UTF8&psc=1)</br>

## Installation

Download the installation script.</br>
```
wget https://raw.githubusercontent.com/ajkelsey/speedcam-st/main/speedcam-st.sh
```

Install</br>
```
./speedcam-st.sh install
```

Remove</br>
```
./speedcan-t.sh remove
```

**Be sure the following directory structure exists:**</br>

```
└── opt
    └── speedcam - Speedcam root directory
        ├── data - CSV file.
        ├── http - Used by ffmpeg_streamer.py and contains index.html.
        ├── imageq - Image persistent file queue.
        ├── images - Images of speeding cars.
        ├── log - Log files.
        ├── video - Video files to be processed.
        └── videoq - Video persistent file queue.
```
##### GPIO Connections</br>

- GPIO 17: Fan relay

- GPIO 22: IR filter

- GPIO 27: IR filter

##### Install:

```bash
sudo apt install python3-apscheduler python3-matplotlib python3-matplotlib \
python3-pandas python3-persist-queue python3-rich
```
```bash
pip install ultralytics --break-system-packages
```

##### Configure:

- /boot/firmware/config.txt
  - Add:
    - Depending on your camera choice, add:
      - HQ: `dtoverlay=imx477,cma-512`
      - Global: `dtoverlay-imx296, cma-512``max_framebuffers=8``camera_auto_detect=0`
- raspiconfig:
  - This is for the temperature sensor.
    - Interface Options > enable 1-wire interface > reboot
- Edit /opt/speedcam/speedcam-config.json accordingly.
- Edit stats.py variables speed_brackets and speed_fines to configure accurate fine estimation for your state. NJ is the default.
- Check that speedcam.service and case_fans.service are enabled and started.

To gain access to the Facebook API, try [this blog post](https://medium.com/nerd-for-tech/automate-facebook-posts-with-python-and-facebook-graph-api-858a03d2b142). I believe things have changed a bit since it was 	posted, but should be very helpful. Here are the notes I have for doing this. I know I struggled getting 	this right at the time and they may not be totally accurate. My script is designed to use a Facebook 	Page. You can create one using your existing account.</br>	

- Create app</br>
  - Choose other than business. Name to be the same as the page you want to create</br>
  - Dashboard > App Settings > App Page > select or create page with the same name as the app.</br>
  - page_id: go page, about tab, page transparency.</br>
  - -Graph API Explorer > Permissions:</br>
    - pages_manage_engagement</br>
    - pages_manage_posts</br>
    - pages_read_engagement</br>
    - pages_read_user_comment</br>
  - Generate token, sign in, select done</br>
  - debug user token, extend user token. never expires</br>
  - user id: settings, business integrations</br>

## Theory of Operation

The speed camera and case fan scripts are run at boot as services; speedcam.service and case_fans.service. 

On startup, the speed camera will initialize the logger, speedcam scheduler, camera, radar, ir_filter, alpr, and facebook facilities. Then launches the vehicle detection thread.

There is a bug somewhere in the software or hardware that causes the files written by the camera to be 0 bytes in size. I found the only way to recover from this is to restart the speedcam service. This happens daily at 3 am via the scheduler, and will do it if it detects a 0 byte file write.

After the initializations, the main loop will be launched. The radar.get_speed() method will be called where the radar serial buffer is checked for data. The output of the radar is continuous when an object is detected and results in multiple speed readings per vehicle. If the gap between radar reports is less than 750ms, the speed camera will consider that reading to be for the same vehicle. 

The camera is slow, and coordinating a still picture to be taken at the correct time is not possible. For this reason, I use video. When there is data to be read from the radar buffer, the camera begins to record video. Reports from the radar are accumulated and then averaged. After the final report, the camaera.stop_video() thread is launched.

If the speed is above the minimum report threshold, the data is added to the daily CSV, and the video will be processed for vehicle detection. This happens in the aplr thread launched during initialization.

The vehicle detection uses a persistent queue to process videos. As each video takes some time to detect, this prevents multiple videos being processed at the same time. It also allows for detection to be resilient across script shutdowns.

For my setup, there is only a part of the image that is clear enough to read the license plates. For this reason, I created a detection zone at line 73 in alpr.py. The video is processed frame by frame. The frame will be checked for objects, and found objects will be checked if they are a vehicle. The vehicles are cropped from the frame using the bounding box and the labeling is applied to the image. Videos recorded from dusk to dawn are not processed because there is not enough light.

Image filenames are kept in a persistent queue for posting to Facebook. A post will occur every hour and upload the images in the queue. Daily at 1 am, the Speeder of the Day is posted, and at 2 am, the chart of daily speeders is posted.

## File Descriptions

|                        |                                                              |
| ---------------------: | ------------------------------------------------------------ |
|            **alpr.py** | Primarily detects vehicles in the captured video. The intent is to have an automatic license plate recognition feature in the future. |
|          **camera.py** | Handles the starting and stopping of video recording.        |
|       **case_fans.py** | Operates the case fans on linux startup. Records temperature to a file every 5 minutes. Not integrated with the speed camera. |
|       **case_temp.py** | Utility that displays a text based graph on screen. Not integrated with the speed camera. |
|            **data.py** | Handles data that is stored in the CSV file.                 |
|        **facebook.py** | Posts to Facebook                                            |
| **ffmpeg_streamer.py** | Utility that streams the camera to a small web server. Helps in pointing the camera during setup. |
|              **fq.py** | File queue used by case_fans.py                              |
|    **http/index.html** | Used by ffmpeg_streamer.py. Be sure to edit the URL contained in this file. |
|       **ir_filter.py** | Operates the camera IR filter. The IR filter is removed for nighttime recording. |
|  **plot_the_plots.py** | Utility that can generate graphs based on recorded data. Outputs to jpeg. plot_the_plots --help |
|           **radar.py** | Communicates with the radar.                                 |
|        **speedcam.py** | Main speed camera file.                                      |
|           **stats.py** | Used to generate the speeder of the day.                     |
|         **vehicle.py** | Vehicle class used to handle the data points for each vehicle detected. |

### speedcam-config.json

|                         |                                                              |
| ----------------------: | ------------------------------------------------------------ |
|         **street_name** | Name of the street camera is on.                             |
|             **inbound** | Cardinal direction for traffic heading towards the camera.   |
|            **outbound** | Cardinal direction for traffic heading away from the camera. |
|                 **lat** | Latitude of camera in decimal. Used to determine sunrise/sunset. |
|                 **lon** | Longitude of camera in decimal. Used to determine sunrise/sunset. |
|            **timezone** | Timezone using the tz database format.                       |
|  **inbound correction** | Speed correction for inbound traffic using chosen speed unit. |
| **outbound correction** | Speed correction for outbound traffic using chosen speed unit. |
|        **angle2street** | The angle the camera is facing the street. 0 is parallel.    |
|        **angle2ground** | The angle the camera is facing the ground. 0 is level. Currently unused. |
|    **min_speed_report** | Minimum speed recorded in the database.                      |
|      **min_speed_post** | Minimum speed required to post to Facebook.                  |
|         **speed_units** | Speed units that are displayed on the image.                 |
|     **camera_facility** | Enable/disable camera recording. 0=off, 1=on                 |
|        **resolution_x** | Horizontal image resolution.                                 |
|        **resolution_y** | Vertical image resolution.                                   |
|      **cam_pre_record** | Length of pre-recording of video prior to radar detection in seconds. |
|     **cam_post_record** | Length of post-recording of video after radar detection in seconds. |
|    **post_to_facebook** | Enable/disable posting to facebook. 0=off, 1=on              |
|                 **vpn** | Enable/disable vpn. 0=off, 1=on (currently unused)           |
|       **logging_level** | DEBUG, INFO, WARNING                                         |
|            **facebook** | Setttings related to Facebook's Graph API                    |
|               **radar** | **device_path**: Confirm this setting for your device.<br />**settings**: Settings sent to the radar. See radar documentation for details. |
