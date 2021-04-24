# With docker
## To run using docker, follow the steps:

1. Check if you have a docker started in you machine, if not, look in the offical site how to start: https://docs.docker.com/get-docker/
2. Is necessary to build the docker image, run the command `docker build -t image-cial-scrapping .` in your terminal in the scrapping_phone_number path.
3. To run the program follow the steps bellow:
  
      a. If you are using Windows, run the command `type websites.txt | docker run -i image-cial-scrapping`
  
      b. If you are using Linux, run the command `cat websites.txt | docker run -i image-cial-scrapping`
  
4. The results will appear in your terminal like in the image bellow:
![image](https://user-images.githubusercontent.com/30561907/115969519-ad933700-a513-11eb-8505-ba8289ad57b7.png)

# Python directly
 
## If you want to run the system without docker, follow the steps:

1. `virtualenv venv`     
2. `venv\Scripts\activate`
3. `pip install -r requirements.txt`

    a. If you are using Windows, run the command `type websites.txt | python -m my_tools`
  
    b. If you are using Linux, run the command `cat websites.txt | python -m my_tools`
    
4. The results will appear in your terminal like in the image bellow:
![image](https://user-images.githubusercontent.com/30561907/115969519-ad933700-a513-11eb-8505-ba8289ad57b7.png)
