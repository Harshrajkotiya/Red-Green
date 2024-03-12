<script>
  import {
    handleResetPassword,
    handleSignin,
    handleSignup,
  } from "./../routes/api/auth/auth";

  let username = "";
  let email = "";
  let password = "";
  let registerEmail = "";
  let registerPassword = "";
  let errorMessage = "";

  function signinclick() {
    console.log("assfgkjjjjj");
    const signIn = document.querySelector("#signInButton");
    const signUp = document.querySelector("#signUpButton");
    const signInForm = document.querySelector(".container .sign-in-form");
    const signUpForm = document.querySelector(".container .sign-up-form");

    const overlay_container = document.querySelector(
      ".container .overlay-container"
    );

    const overlay = document.querySelector(
      ".container .overlay-container .overlay"
    );

    overlay_container.style.transform = "translate(100%) rotateY(180deg) ";
    overlay.style.transform = "translateX(-50%)";
    signInForm.classList.add("active");
    signUpForm.classList.remove("active");
  }

  function signupclick() {
    const signIn = document.querySelector("#signInButton");
    const signUp = document.querySelector("#signUpButton");
    const signInForm = document.querySelector(".container .sign-in-form");
    const signUpForm = document.querySelector(".container .sign-up-form");

    const overlay_container = document.querySelector(
      ".container .overlay-container"
    );

    const overlay = document.querySelector(
      ".container .overlay-container .overlay"
    );

    overlay_container.style.transform = "translate(0%) rotateY(0deg)";
    overlay.style.transform = "translateX(0%)";
    signUpForm.classList.add("active");
    signInForm.classList.remove("active");
  }
</script>

<section>
  <div class="container">
    <div class="form sign-in-form">
      <div class="wrapper">
        <form
          on:submit|preventDefault={() =>
            handleSignup(registerEmail, registerPassword, username)}
        >
          <h1>Create Account</h1>
          <i
            class="mt-2 fa fa-user-o input_icon"
            style="position: absolute;
                      left: 15%;
                      z-index: 99;"
          />
          <input
            type="text"
            placeholder="Username"
            style="padding-left: 2rem!important;"
            bind:value={username}
            required
          />

          <i
            class="mt-2 fa fa-envelope-o input_icon"
            style="position: absolute;
                      left: 15%;
                      z-index: 99;"
          />

          <input
            type="email"
            placeholder="Email"
            style="padding-left: 2rem!important;"
            bind:value={registerEmail}
            required
          />

          <i
            class="mt-2 fa fa-key input_icon"
            style="position: absolute;
                    left: 15%;
                    z-index: 99;"
          />
          <input
            type="password"
            placeholder="Password"
            style="padding-left: 2rem!important;"
            bind:value={registerPassword}
            required
            minlength={8}
          />

          <button type="submit">Sign Up</button>
          <div class="mt-4">
            <p style="color: #9C99B2">By signing up, I agree to</p>
            <a href="#">Derivedged Terms of Service</a>
            <span style="color:#9C99B2">and</span>
            <a href="#">Privacy Policy</a>
          </div>
        </form>
      </div>
    </div>

    <div class="form sign-up-form active">
      <div class="wrapper">
        <form
          data-sveltekit-reload
          action="/futures/oi_interpretation"
          on:submit|preventDefault={() => handleSignin(email, password)}
        >
          <h1>Login</h1>

          <i
            class=" mt-2 input_icon"
            aria-hidden="true"
            style="position: absolute;right:80%;"
          />
          <!-- <input type="email">
            <i class="fa fa-key mt-2" aria-hidden="true" style="position: absolute;right:80%; color:#6C6F71"></i> -->

          <i
            class="mt-2 fa fa-envelope-o input_icon"
            style="position: absolute;
                        left: 15%;
                        z-index: 99;"
          />

          <input
            class="px-2 py-2 border-left-0 border"
            type="email"
            placeholder="Email"
            id="example-search-input"
            style="padding-left: 2rem!important;"
            bind:value={email}
            required
          />

          <i
            class="mt-2 fa fa-key input_icon"
            style="position: absolute;
                      left: 15%;
                      z-index: 99;"
          />

          <input
            type="password"
            placeholder="Password"
            style="padding-left: 2rem!important;"
            bind:value={password}
            required
            minlength={8}

          />

          <div class="d-flex">
            <input
              type="checkbox"
              class="mx-0 me-2"
              name="Remember me"
              style="width: 15px;"
            /><label class="mt-1">Remember me</label> <br />
            <a
              href="#"
              on:click|preventDefault={handleResetPassword}
              class="mt-1"
              style="margin-left: 18%;color: #000000;"
              >Forget password
            </a>
          </div>
          <button type="submit">LOGIN</button>
          <p style="color: #9C99B2" class="mt-4">By signing up, I agree to</p>
          <a href="#">Derivedged Terms of Service</a>
          <span style="color:#9C99B2">and</span>
          <a href="#">Privacy Policy</a>
        </form>
      </div>

      <!-- </div> -->
    </div>

    <div class="overlay-container">
      <div class="overlay">
        <div class="overlay-left">
          
          <h4>
            We are <span style="color:#ED1A3B">Red</span>
            <span style="color:#009B66">Green</span>
          </h4>
          <h1 >Hello Friend!</h1>
          <h6>Enter your personal details and start journey with us</h6>
          <button id="signInButton" on:click={signinclick}>Sign Up</button>
        </div>
        <div class="overlay-right" style="transform:rotateY(180deg)">
          <!-- <span><h1 style="transform:rotateY(180deg) !important;">Please, Log In</h1></span>
            <p style="transform:rotateY(180deg) !important;">or</p> -->
            <h4>
              We are <p>
                <span style="color:#ED1A3B">Red</span>
                <span style="color:#009B66">Green</span>
              </p>
            </h4>
          <!-- <h1>Hello Friend!</h1> -->
          <h6>Welcome Back, Please login to Your account</h6>

          <button id="signUpButton" on:click={signupclick}>Log In</button>
        </div>
        <!-- </div> -->
      </div>
    </div>
  </div>
</section>

<!-- *******************   -->
<!--  This Code is for only the floating card in right bottom corner -->

<!-- ********************  -->
<style>
  * {
    padding: 0;
    margin: 0;
    box-sizing: border-box;
    /* font-family: "Inter"; */
  }
  section {
    min-height: 95vh;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .container {
    box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.199);
    padding: 50px 30px;
    border-radius: 10px;
    min-width: 800px;
    max-width: 1000px;
    min-height: 500px;
    margin: 0 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #f6f5f7;
    position: relative;
    overflow: hidden;
  }

  .container .form {
    position: absolute;
    top: 0;
    text-align: center;
    padding: 0 20px;
    width: 50%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #f6f5f7;
    transition: 0.7s ease-in-out transform;
    overflow: hidden;
    font-family: "Inter";
  }
  .container .form.sign-in-form {
    left: 0;
  }
  .container .form.sign-up-form {
    right: 0;
  }
  .container .form .wrapper {
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: 0.7s ease-in-out transform;
    background-color: #ffffff;
  }
  .container .form.sign-in-form .wrapper {
    transform: translateX(100%);
  }
  .container .sign-in-form.active .wrapper {
    transform: translateX(0);
  }
  .container .form.sign-up-form .wrapper {
    transform: translateX(-100%);
  }
  .container .sign-up-form.active .wrapper {
    transform: translateX(0);
  }
  .container .form h1 {
    margin-bottom: 10px;
    color: #1e1f4b;
    font-family: "Inter";
    font-style: normal;
    font-weight: 700;
    font-size: 24px;
    line-height: 29px;
  }
  .container .form p {
    /* font-family: "Roboto"; */
    font-family: "Inter";
    font-weight: 500;
    font-size: 14px;
    text-transform: capitalize;
    line-height: 25px;
    /* margin-bottom: 30px; */
  }
  .container .form input {
    display: block;
    width: 300px;
    margin: 0 auto;
    margin-bottom: 15px;
    height: 35px;
    font-family: "Montserrat";
    font-size: 14px;
    padding-left: 15px;
    /* border: none;
  background-color: rgba(199, 197, 197, 0.425);
  outline: none; */

    background: #ffffff;
    border: 1px solid #e7e6ef;
    border-radius: 4px;
  }

  .container .form input::placeholder {
    color: rgba(0, 0, 0, 0.658);
  }
  .overlay-container .overlay button,
  .container .form button {
    padding: 10px 50px;
    outline: none;
    font-family: "Inter";
    font-size: 18px;
    background-color: #009b66;
    cursor: pointer;
    color: #f6f5f7;
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 5px;
  }
  .container .overlay-container {
    position: absolute;
    background-color: #35433e;
    left: 0;
    top: 0;
    width: 50%;
    height: 100%;
    overflow: hidden;
    transition: 0.7s ease-in-out transform;
    font-family: "Inter";
  }

  .container .overlay-container .overlay {
    background: url("../images/login_img.svg");
    background-size: cover;
    background-position: center center;
    position: absolute;
    left: 0%;
    /* background-color: rebeccapurple; */
    width: 200%;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    transition: 0.7s ease-in-out transform;
    z-index: 1;
  }
  .container .overlay::after {
    content: "";
    position: absolute;
    height: 100%;
    width: 100%;
    left: 0;
    top: 0;
    background-color: #35433e;
    z-index: -1;
    opacity: 0.9;
  }
  .overlay-container .overlay .overlay-left,
  .overlay-container .overlay .overlay-right {
    flex-basis: 50%;
    text-align: center;
    color: #ffffff;
  }
  .overlay-container .overlay .overlay-right h4 {
    font-family: "Inter";
    font-style: normal;
    font-weight: 700;
    font-size: 40px;
    line-height: 45px;
    margin-left: 7%;
    /* or 120% */
    display: block;
    align-items: center;
    text-align: center;
    color: #ffffff;
  }
  /* .overlay-container .overlay .overlay-left {
} */
  .overlay-container h1 {
    /* font-family: "Montserrat";
  font-size: 40px;
  font-weight: 300;
  color: white; */

    font-family: "Inter";
    font-style: normal;
    font-weight: 700;
    font-size: 48px;
    line-height: 58px;

    /* identical to box height, or 120% */
    color: #ffffff;
  }
  .overlay-container .overlay h6 {
    /* color: white;
  font-family: "Roboto";
  font-size: 25px;
  font-weight: 300; */

    font-family: "Inter";
    font-style: normal;
    font-weight: 600;
    font-size: 16px;
    line-height: 24px;
    /* or 150% */
    text-align: center;
    color: #ffffff;
    /* opacity: 0.5; */
  }
  .overlay-container .overlay button {
    background-color: white;
    color: #35433e;
    margin-top: 20px;
  }

  .input_icon {
    color: #3d3d3d;
  }
  /* ********************* */
  /* This Code is for only the floating card in right bottom corner */
  /* ********************** */

  @import url("https://fonts.googleapis.com/css2?family=Roboto+Mono&display=swap");
  * {
    padding: 0;
    margin: 0;
    -webkit-box-sizing: border-box;
    box-sizing: border-box;
  }

  a {
    color: var(--color-4);
    text-decoration: none;
  }
  #webCifar-sidebox {
    position: absolute;
    right: 0px;
    bottom: 0px;
    overflow-x: clip;
    width: 300px;
  }
  #webCifar {
    --color-1: #17bcb4;
    --color-2: #24252a;
    --color-3: #244044;
    --color-4: #f3f8f7;
    background: var(--color-2);
    display: inline-block;
    color: var(--color-4);
    padding: 10px 17px;
    border-radius: 6px;
    font-family: "Roboto Mono", monospace;
    text-align: center;
    position: absolute;
    right: 5px;
    bottom: 5px;
    -webkit-transform: translateX(calc(100% + 5px));
    transform: translateX(calc(100% + 5px));
    -webkit-transition: 0.5s ease-out transform;
    transition: 0.5s ease-out transform;
    z-index: 4;
  }

  #webCifar:active {
    -webkit-transform: translateX(0);
    transform: translateX(0);
  }

  #webCifar .logo {
    font-size: 25px;
  }

  #webCifar .author {
    margin-top: 10px;
    margin-bottom: 20px;
  }

  #webCifar .author span {
    background-color: var(--color-3);
    padding: 3px;
    border-radius: 4px;
  }

  #webCifar .items {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-align: start;
    -ms-flex-align: start;
    align-items: start;
    -webkit-box-pack: center;
    -ms-flex-pack: center;
    justify-content: center;
    -webkit-box-orient: vertical;
    -webkit-box-direction: normal;
    -ms-flex-direction: column;
    flex-direction: column;
  }

  #webCifar .item {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    -webkit-box-pack: center;
    -ms-flex-pack: center;
    justify-content: center;
    gap: 10px;
    padding: 5px;
    border-radius: 4px;
    text-align: left;
  }

  #webCifar .item:hover {
    background-color: var(--color-3);
  }

  #webCifar svg {
    max-width: 20px;
  }

  #webCifar .close {
    position: absolute;
    display: inline-block;
    height: 30px;
    width: 30px;
    right: 5px;
    top: 5px;
    padding: 5px;
    background-color: var(--color-3);
    border-radius: 50%;
    font-size: 20px;
    cursor: pointer;
  }

  #webCifar-icon {
    --color-2: #24252a;
    --color-3: #244044;
    font-family: "Roboto Mono", monospace;
    text-align: left;
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    -webkit-box-pack: center;
    -ms-flex-pack: center;
    justify-content: center;
    background-color: var(--color-2);
    color: white;
    width: -webkit-fit-content;
    width: -moz-fit-content;
    width: fit-content;
    padding: 5px;
    border-radius: 4px;
    gap: 5px;
    margin: 5px;
    cursor: pointer;
    z-index: 1;
    position: relative;
    right: -27%;
  }

  #webCifar-icon svg {
    max-width: 20px;
  }
</style>
