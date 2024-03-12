<script>
  import { onMount } from "svelte";

  onMount(() => {
    const phoneInputField = document.querySelector("#phone");
      const phoneInput = window.intlTelInput(phoneInputField, {
        utilsScript:
          "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.js",
      });
  });
</script>

<div class="form-body">
  <div class="row">
    <div class="form-holder">
      <div class="form-content">
        <div class="form-items">
          <h3>We love listening to you!</h3>
          <form class="requires-validation" novalidate>
            <div class="col-md-12">
              <input
                class="form-control"
                type="text"
                name="name"
                placeholder="Name"
                required
              />
              <div class="valid-feedback">Username field is valid!</div>
              <div class="invalid-feedback">
                Username field cannot be blank!
              </div>
            </div>

            <div class="col-md-12">
              <input
                class="form-control"
                type="email"
                name="email"
                placeholder="E-mail Address"
                required
              />
              <div class="valid-feedback">Email field is valid!</div>
              <div class="invalid-feedback">Email field cannot be blank!</div>
            </div>
            <div class="col-md-12 mt-3" style="display:grid;">
              <input
                class="form-control"
                type="tel"
                id="phone"
                placeholder="e.g. +1 702 123 4567"
                value="+1 "
            
              />
            </div>
            <div class="col-md-12">
              <input
                class="form-control"
                type="text"
                name="subject"
                placeholder="Subject"
                required
              />
            </div>

            <div class="col-md-12">
              <textarea
                class="form-control mt-3 bg-white"
                placeholder="Your Message"
                rows="3"
                required
              />
            </div>

            <div class="form-check">
              <input
                class="form-check-input"
                type="checkbox"
                value=""
                id="invalidCheck"
                required
              />
              <label class="form-check-label"
                >I confirm that all data are correct</label
              >
              <div class="invalid-feedback">
                Please confirm that the entered data are all correct!
              </div>
            </div>

            <div class="form-button mt-3">
              <button id="submit" type="submit" class="btn btn-primary"
                >Submit</button
              >
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
 

  .form-holder {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    min-height: 70vh;
  }

  .form-holder .form-content {
    position: relative;
    text-align: center;
    display: -webkit-box;
    display: -moz-box;
    display: -ms-flexbox;
    display: -webkit-flex;
    display: flex;
    -webkit-justify-content: center;
    justify-content: center;
    -webkit-align-items: center;
    align-items: center;
    padding: 60px;
  }

  .form-content .form-items {
    border: 3px solid #fff;
    padding: 40px;
    display: inline-block;
    width: 100%;
    min-width: 540px;
    -webkit-border-radius: 10px;
    -moz-border-radius: 10px;
    border-radius: 10px;
    text-align: left;
    -webkit-transition: all 0.4s ease;
    transition: all 0.4s ease;
  }

  .form-content h3 {
    color: #fff;
    text-align: left;
    font-size: 28px;
    font-weight: 600;
    margin-bottom: 5px;
  }

  .form-content h3.form-title {
    margin-bottom: 30px;
  }

  .form-content p {
    color: #fff;
    text-align: left;
    font-size: 17px;
    font-weight: 300;
    line-height: 20px;
    margin-bottom: 30px;
  }

  .form-content label,
  .was-validated .form-check-input:invalid ~ .form-check-label,
  .was-validated .form-check-input:valid ~ .form-check-label {
    color: #fff;
  }

  .form-content input[type="text"],
  .form-content input[type="password"],
  .form-content input[type="email"],
  .form-content select {
    width: 100%;
    padding: 9px 20px;
    text-align: left;
    border: 0;
    outline: 0;
    border-radius: 6px;
    background-color: #fff;
    font-size: 15px;
    font-weight: 300;
    color: #8d8d8d;
    -webkit-transition: all 0.3s ease;
    transition: all 0.3s ease;
    margin-top: 16px;
  }

  .btn-primary {
    background-color: #6c757d;
    outline: none;
    border: 0px;
    box-shadow: none;
  }

  .btn-primary:hover,
  .btn-primary:focus,
  .btn-primary:active {
    background-color: #495056;
    outline: none !important;
    border: none !important;
    box-shadow: none;
  }

  .form-content textarea {
    position: static !important;
    width: 100%;
    padding: 8px 20px;
    border-radius: 6px;
    text-align: left;
    background-color: #fff;
    border: 0;
    font-size: 15px;
    font-weight: 300;
    color: #8d8d8d;
    outline: none;
    resize: none;
    height: 120px;
    -webkit-transition: none;
    transition: none;
    margin-bottom: 14px;
  }

  .form-content textarea:hover,
  .form-content textarea:focus {
    border: 0;
    background-color: #ebeff8;
    color: #8d8d8d;
  }

  .mv-up {
    margin-top: -9px !important;
    margin-bottom: 8px !important;
  }

  .invalid-feedback {
    color: #ff606e;
  }

  .valid-feedback {
    color: #2acc80;
  }

   .intl-tel-input .form-control {
    /* padding-left: 30px !important; */
    width:100%;
  }
  .intl-tel-input .flag-dropdown .selected-flag {
    /* padding: 11px 16px 11px 6px; */
    /* margin: 10px; */
  }
  .intl-tel-input {
    z-index: 99;
    /* width: 100%; */
  }
  .iti-flag {
    /* box-shadow: none; */
  }
  .intl-tel-input .selected-flag:focus {
    /* outline: none; */
  }
  .iti{
    display: flex !important;
  }
</style>
