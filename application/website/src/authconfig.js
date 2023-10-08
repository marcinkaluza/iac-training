/* eslint-disable */
// WARNING: DO NOT EDIT. This file is automatically generated by AWS Amplify. It will be overwritten.
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

export default amplifyConfig;