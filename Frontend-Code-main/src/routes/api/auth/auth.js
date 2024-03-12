import { onDestroy } from "svelte";
import { auth } from "../../../firebase";
import {
  createUserWithEmailAndPassword,
  sendPasswordResetEmail,
  signInWithEmailAndPassword,
  updatePassword,
} from "firebase/auth";

let userEmail = "";
let errorMessage = "";

async function handleSignup(email, password, username) {
  // @ts-ignore
  console.log("in signup....");
  try {
    const userCredential = await createUserWithEmailAndPassword(
      auth,
      email,
      password,
      // @ts-ignore
      {
        displayName: username,
      }
    );
    // Handle the registration success
    // ...
    console.log("registered", userCredential);
  } catch (error) {
    errorMessage = error.message;
    console.log(errorMessage);
  }
}

function handleSignin(email, password) {
  // @ts-ignore
  signInWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      // Handle the login success
      // ...
      console.log("logged in..", userCredential);
      // @ts-ignore
    })
    .catch((error) => {
      errorMessage = error.message;
      console.log(errorMessage);
    });
}

function handleResetPassword() {
  const user = auth.currentUser;

  // Password updated successfully
  // Send password reset email to the user's email address
  sendPasswordResetEmail(auth, user.email)
    .then(() => {
      // Password reset email sent successfully
      console.log("mail sent");
    })
    .catch((error) => {
      // Handle the password reset email send error
      console.log("unable to sent mail", error);
    });
}

export { handleSignup, handleSignin, handleResetPassword };
