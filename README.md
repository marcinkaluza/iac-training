# Welcome to Tech-U CDK training!

This repository conatains code for a sample serverless web application. All that is missing is AWS infrastructure required
to run it on, which is where you come in. Your task is to create a CDK stack containing all resources as per the diagram below.

![webapp](Application.png)

# Initializing the project

First clone this repository to your local machine:

```
git clone https://github.com/marcinkaluza/iac-training.git
```

Once the repo has been cloned, open terminal in the `iac-training` directory and execute following commands:

```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

Make sure that you have valid AWS credentials available by executinig
```
aws sts get-caller-identity
```
Assuming everything worked as expected, you can try to deploy the application by executing ```cdk deploy```. As we haven't defined any resources yet, the application will not provision anything but it will allow to check that everything is working.

# Building the website

Before you build the infrastructure, you will need to build the production version of the website. In order to achieve that, open terminal window in the 
```iac-training/application/website``` directory and execute following commands:

```
$ npm i
$ npm run build
```

# Building the infrastructure

Open visual studio code. In the ```iac-training``` directory execute 
```
$ code .
```
Once the solution has been opened, open the [application_stack.py](./application/application_stack.py) file and follow the instruction within it.

# Rebuilding the web application

If you were succesfull in deploying the application, accessing the cloudfront URL may present a website, but the website is not quite working yet. In order to make it functional we need to update parameters in the ```iac-training/application/website/src/authconfig.js``` file. This file contains id of the cognito user pool and the application id which our CDK code creates. 

```
const amplifyConfig = {
  Auth: {
    // REQUIRED - Amazon Cognito Region
    region: "eu-west-1",
    // OPTIONAL - Amazon Cognito User Pool ID
    userPoolId: "eu-west-1_yaPYQDLMd",
    // OPTIONAL - Amazon Cognito Web Client ID (26-char alphanumeric string)
    userPoolWebClientId: "4gj6r4sdhqlhmh4688aj58cr7s",
    // OPTIONAL - Enforce user authentication prior to accessing AWS resources or not
    mandatorySignIn: false,
    // OPTIONAL - This is used when autoSignIn is enabled for Auth.signUp
    // 'code' is used for Auth.confirmSignUp, 'link' is used for email link verification
    signUpVerificationMethod: "code", // 'code' | 'link'
    // OPTIONAL - Manually set the authentication flow type. Default is 'USER_SRP_AUTH'
    authenticationFlowType: "USER_SRP_AUTH",
  },
};
```

In order for the application to work, we need to update ```userPoolId``` and ```userPoolWebClientId``` which should be both outputs of your CDK application. Once you have updated the file, rebuild the web application using ```npm run build``` command and redeploy your CDK app. Once redeployed, you should have a working web app.