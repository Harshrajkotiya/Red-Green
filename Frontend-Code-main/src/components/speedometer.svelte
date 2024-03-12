<script>
  import { onMount, afterUpdate } from "svelte";

  export let stock_per;
  // let stock_per;
  var mymodel = "";
  const numbers = [];
  var setid = 0;
  var step_count = 0;
  const colors = [];
  var prev_count;
  let first = true;
  var cursor;
  const update_Speedometer = (my_per) => {
    console.log("update_Speedometer trigger");
    // no. of div caount calc
    step_count = Math.floor(37 * (my_per / 100));

    // for give the color to all circular box
    if (prev_count) {
      if (prev_count < step_count) {
        console.log(prev_count < step_count);
        colors.slice(prev_count, step_count).forEach((i, index) => {
          setTimeout(() => {
            cursor = document.getElementById(`i${colors.indexOf(i)}`);
            cursor.style.backgroundColor = i;
          }, (1000 / (step_count - prev_count)) * (index + 2));
        });
      } else {
        // let i = prev_count
        let i = colors.slice(step_count, prev_count);
        i.reverse().forEach((i, index) => {
          {
            setTimeout(() => {
              cursor = document.getElementById(`i${colors.indexOf(i)}`);
              cursor.style.backgroundColor = "rgb(54, 54, 51)";
            }, (1000 / (prev_count - step_count)) * (index + 2));
          }
        });
        // prev_count=step_count
      }
    } else if (prev_count == undefined || prev_count == 0) {
      // console.log("this is running");
      colors.slice(0, step_count).forEach((i, index) => {
        setTimeout(() => {
          var cursor = document.getElementById(`i${colors.indexOf(i)}`);
          cursor.style.backgroundColor = i;
        }, (1000 / step_count) * (index + 2));
      });

      // console.log(colors.slice(0,step_count));
    }

    // if(first){

    // }
    // anim of pointer and circular line
    if (my_per == 0) {
      border_hider.style.transform = `rotate(${180 * (my_per / 100)}deg) `;
      pointer.style.transform = `rotate(${-90 + 180 * (my_per / 100)}deg)`;
    } else {
      border_hider.style.transform = `rotate(${180 * (my_per / 100)}deg) `;
      pointer.style.transform = `rotate(${-90 + 180 * (my_per / 100)}deg)`;
    }
    prev_count = step_count;
    console.log("current", step_count);
  };

  onMount(() => {
    // declaration of all page object
    // stock_per = 0

    var border_hider = document.getElementById("border_hider");
    var speed_body = document.getElementById("hi");
    var mycont = document.getElementById("grad_container");
    var pointer = document.getElementById("pointer");

    // this given query below, width and height is for div sizing and top and left is basically margin between outer circle and current div tag  and  transform-origin should be equal to distance between div and center of circle
    // all no of angle for pointer
    for (var i = -90; i <= 90; i += 5) {
      mymodel += `<div id=i${setid} style="z-index:4; position: absolute; height: 15px; width: 5px; top:35px; left: 35px; background-color: rgb(54, 54, 51); transform-origin: 115px 115px; transform: rotate(${i}deg) translateX(112.5px);;"></div>`;
      setid += 1;
    }
    // console.log(numbers.length);  # 37
    speed_body.innerHTML += mymodel;

    const gradientColors = [
      { r: 239, g: 24, b: 7 }, // Red
      { r: 247, g: 114, b: 52 }, // Orange
      { r: 253, g: 232, b: 35 }, // Yellow
      { r: 123, g: 243, b: 147 }, // Green
      { r: 1, g: 255, b: 254 }, // Blue
    ];

    // Define the total number of steps in the gradient range
    const totalSteps = 40;

    // Calculate the number of steps for each color section
    const stepsPerSection = Math.floor(
      totalSteps / (gradientColors.length - 1)
    );

    // Create a loop to generate the gradient colors
    for (let i = 0; i < gradientColors.length - 1; i++) {
      // Get the starting and ending colors for this section
      const startColor = gradientColors[i];
      const endColor = gradientColors[i + 1];

      // Calculate the step values for the red, green, and blue channels
      const rStep = (endColor.r - startColor.r) / stepsPerSection;
      const gStep = (endColor.g - startColor.g) / stepsPerSection;
      const bStep = (endColor.b - startColor.b) / stepsPerSection;

      // Create a loop to generate the gradient colors for this section
      for (let j = 0; j < stepsPerSection; j++) {
        // Calculate the red, green, and blue values for this step
        const r = Math.round(startColor.r + j * rStep);
        const g = Math.round(startColor.g + j * gStep);
        const b = Math.round(startColor.b + j * bStep);

        // Add the color to the array
        colors.push(`rgb(${r}, ${g}, ${b})`);
      }
    }

    update_Speedometer(0);
  });
  afterUpdate(() => {
    if (first) {
      update_Speedometer(0);
      setTimeout(() => {
        update_Speedometer(stock_per);
        first = false;
      }, 1);
    } else {
      update_Speedometer(stock_per);
    }
  });
</script>

<div id="speed_body">
  <div class="upper_speed" id="hi">
    <div class="myborder" />

    <div class="parameter">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="180px"
        viewBox="0 0 191 101.5"
      >
        <defs>
          <style>
            .cls-1 {
              fill: #2ff7f7;
            }

            .cls-1,
            .cls-2,
            .cls-3,
            .cls-4,
            .cls-5 {
              opacity: 0.2;
            }

            .cls-2 {
              fill: #00ff91;
            }

            .cls-3 {
              fill: #ff0;
            }

            .cls-4 {
              fill: #f15a24;
            }

            .cls-5 {
              fill: red;
            }
          </style>
        </defs>
        <g id="Layer_2" data-name="Layer 2">
          <g id="Layer_2-2" data-name="Layer 2">
            <path
              class="cls-1"
              d="M191,95.5q0,3-.19,6H95l80.35-58.38A94.94,94.94,0,0,1,191,95.5Z"
            />
            <path
              class="cls-2"
              d="M175.35,43.12,95,101.5,126.32,5.09A95.56,95.56,0,0,1,175.35,43.12Z"
            />
            <path
              class="cls-3"
              d="M126.32,5.09,95,101.5,63.78,5.41a95.77,95.77,0,0,1,62.54-.32Z"
            />
            <path
              class="cls-4"
              d="M95,101.5,15.32,43.61A95.69,95.69,0,0,1,63.78,5.41Z"
            />
            <path
              class="cls-5"
              d="M95,101.5H.19q-.19-3-.19-6A95,95,0,0,1,15.32,43.61Z"
            />
          </g>
        </g>
      </svg>
    </div>

    <div id="border_hider" class="myborder_hider" />

    <div id="pointer" class="triangle_pointer">
      <svg width="10" height="80">
        <defs>
          <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#FFA500" />
            <stop offset="100%" stop-color="#FF4500" />
          </linearGradient>
        </defs>
        <polygon points="0,80 5,0 10,80" style="fill:url(#gradient)" />
      </svg>
    </div>

    <div class="guage_center" />
  </div>

  <!-- lower part of circle -->
  <div class="speed_lower">
    <p class="yellow_lable">Market Mode</p>

    <p class="blue_lable">VERY BULLISH</p>

    <p class="yellow_lable">based on two anlysis, 09/02/2024</p>
  </div>
</div>

<style>
  :root {
    --speed_width: 300px;
    --speed_height: 300px;
    --speed_bg: rgb(6, 6, 6);
    --grad_margin: 8px;
    --grad_width: 15px;
    --par_width: 180px;
    --point_height: 80px;
    --point_width: 10px;
    --center_width: 20px;
  }

  .myborder_hider {
    z-index: 2;
    position: absolute;
    border-radius: calc(var(--speed_height) / 2) calc(var(--speed_height) / 2)
      0px 0px;
    overflow-y: hidden;
    width: var(--speed_width);
    height: calc(var(--speed_height) / 2);
    top: 0px;
    transform-origin: bottom center;
    transform: rotate(0deg);
    background-color: var(--speed_bg);
    transition: all 2s;
  }

  #grad_container {
    /* position: relative; */
    display: flex;
  }

  .parameter {
    z-index: 3;
    position: absolute;
    bottom: -6px;
    width: var(--speed_width);
    /* left: 50px; */
  }

  .upper_speed {
    /* z-index: -3; */
    position: relative;
    width: var(--speed_width);
    height: calc(var(--speed_height) / 2);
    border-radius: calc(var(--speed_height) / 2) calc(var(--speed_height) / 2)
      0px 0px;
    top: 0px;
    left: 0px;
  }

  .speed_lower {
    z-index: 10;
    position: relative;
    bottom: 0;
    left: 0;
    width: var(--speed_width);
    height: calc(var(--speed_height) / 2);
    padding: 20px;
    background-color: transparent;
  }

  .guage_center {
    z-index: 4;
    width: var(--center_width);
    height: var(--center_width);
    border-radius: 50%;
    position: absolute;
    background: rgb(237, 73, 9);
    top: calc(var(--speed_height) / 2 - var(--center_width) / 2);
    box-shadow: 0px 0px 15px 0px rgb(237, 73, 9);
    left: calc(var(--speed_width) / 2 - var(--center_width) / 2);
  }

  .triangle_pointer {
    z-index: 4;
    position: absolute;
    /* width: 0; */
    /* height: 0; */
    top: calc(var(--speed_height) / 2 - var(--point_height));
    left: calc(var(--speed_width) / 2 - var(--point_width) / 2);
    /* border-right: 4px solid transparent; */
    /* border-bottom: 80px solid red; */
    /* border-left: 4px solid transparent; */
    transform: rotate(-90deg);
    transform-origin: 4px 80px;
    transition: all 2s;
  }

  #speed_body {
    border-radius: 50%;
    width: var(--speed_width);
    height: var(--speed_height);
    background-color: var(--speed_bg);
    box-shadow: 0px 0px 7px 0.5px yellow;
    /* position: relative; */
  }

  .myborder {
    z-index: 1;
    border-radius: calc(var(--speed_height) / 2 - var(--grad_margin))
      calc(var(--speed_height) / 2 - var(--grad_margin)) 0px 0px;
    width: calc(var(--speed_width) - 2 * var(--grad_margin));
    height: calc(var(--speed_height) / 2 - var(--grad_margin));
    /* inset: 20px; */
    /* box-shadow: inset 0px 0px 5px 10px white; */
    top: var(--grad_margin);
    /* left: 5px; */
    background: linear-gradient(
      to right,
      rgb(239, 24, 7),
      rgb(247, 114, 52),
      rgb(253, 232, 35),
      rgb(123, 243, 147),
      rgb(1, 255, 254)
    );
    background-origin: border-box;

    position: relative;
    /* overflow: hidden; */
    box-shadow: inset 0px 0px 10px 10px rgb(6, 6, 6);
  }

  .myborder::before {
    box-shadow: 0px 0px 10px 5px rgb(6, 6, 6);
    border-radius: calc(
        (var(--speed_height) / 2 - var(--grad_margin)) - var(--grad_width)
      )
      calc((var(--speed_height) / 2 - var(--grad_margin)) - var(--grad_width))
      0px 0px;
    position: absolute;
    content: "";
    /* width: 250px; */
    height: 125px;
    width: calc(
      (var(--speed_width) - 2 * var(--grad_margin)) - 2 * var(--grad_width)
    );
    height: calc(
      (var(--speed_height) / 2 - var(--grad_margin)) - var(--grad_width)
    );
    top: var(--grad_width);
    /* right: 20px; */
    left: var(--grad_width);
    /* bottom: 22.5px; */
    background: rgb(6, 6, 6);
    /* background-color: #0f0; */
  }
  

  .wrapper {
    box-sizing: border-box;
    margin: 1rem auto 2rem;
    padding: 2rem;
    width: 90%;
    max-width: 25rem;
    background: linear-gradient(#222, #222),
      linear-gradient(to right, red, purple);
    border: 5px solid transparent;
    background-repeat: no-repeat;
    background-origin: padding-box, border-box;
  }

  .bent-container {
    border-radius: 50% / 100%;
    transform: skew(-2deg);
    background-color: #f2f2f2;
    padding: 20px;
  }

  .yellow_lable {
    margin: 4px;
    font-size: 8px;
    color: rgb(202, 202, 87);
    text-align: center;
  }

  .blue_lable {
    margin: 4px;
    font-size: 16px;
    font-weight: 600;
    color: rgb(150, 213, 252);
    text-align: center;
  }

  #container {
    margin: 20px;
    width: 200px;
    height: 100px;
  }
  .circle {
    width: 200px;
    height: 200px;
    border-radius: 50%;
    border: 10px solid transparent;
    background: linear-gradient(
      90deg,
      orange,
      #0f0,
      black,
      rgb(4, 4, 3),
      grey,
      blue
    );
    background-size: 100% 100%, auto;
    background-origin: border-box, padding-box;
    box-shadow: inset 0px 0px 20px rgba(0, 0, 0, 0.5);
  }
</style>
