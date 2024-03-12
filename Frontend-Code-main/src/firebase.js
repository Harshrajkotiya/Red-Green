import {getAuth} from 'firebase/auth';
import {getFirestore} from 'firebase/firestore';
import { initializeApp } from 'firebase/app';

const firebaseConfig = {
  apiKey: "AIzaSyAnOmlLvVUksnxKF5ZfooNuYA8PZeAVpic",
  authDomain: "identity-platform-demo-194c1.firebaseapp.com",
  projectId: "identity-platform-demo-194c1",
  storageBucket: "identity-platform-demo-194c1.appspot.com",
  messagingSenderId: "989669579845",
  appId: "1:989669579845:web:f335b835d325fb7d87172c",
  measurementId: "G-C84RXGKQK4"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const firestore = getFirestore(app);

export { auth, firestore };