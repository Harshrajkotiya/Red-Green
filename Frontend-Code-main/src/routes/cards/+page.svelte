<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.0/jquery.min.js"></script>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
<!-- <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"></script> -->




<div class="sub_back">
    
    
    <div class="circle">
    <img src="images/lap.svg" style="width:30%; position:absolute; top:20%; width:70%; right:15%" alt="">
    <div class="symbol s1"><a href="" data-bs-toggle="modal" data-bs-target="#exampleModal"><img src="images/lightbulb.svg" style="width:70%; position:absolute; top:15%; right:15%; transform: rotate(90deg)" alt=""> </a></div>
    <div class="symbol s2"><a href="" data-bs-toggle="modal" data-bs-target="#exampleModal"><img src="images/lightbulb.svg" style="width:70%; position:absolute; top:15%; right:15%; transform: rotate(54deg)" alt=""></a></div>
    <div class="symbol s3"><a href="" data-bs-toggle="modal" data-bs-target="#exampleModal"><img src="images/lightbulb.svg" style="width:70%; position:absolute; top:15%; right:15%; transform: rotate(18deg)" alt=""></a></div>
    <div class="symbol s4"><a href="" data-bs-toggle="modal" data-bs-target="#exampleModal"><img src="images/lightbulb.svg" style="width:70%; position:absolute; top:15%; right:15%; transform: rotate(-18deg)" alt=""></a></div>
    <div class="symbol s5"><a href="" data-bs-toggle="modal" data-bs-target="#exampleModal"><img src="images/lightbulb.svg" style="width:70%; position:absolute; top:15%; right:15%; transform: rotate(-54deg)" alt=""></a></div>
    <div class="symbol s6"><a href="" data-bs-toggle="modal" data-bs-target="#exampleModal"><img src="images/lightbulb.svg" style="width:70%; position:absolute; top:15%; right:15%; transform: rotate(-90deg)" alt=""></a></div>

</div>




</div>

<div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">Modal title</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <p>Modal body text goes here.</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button type="button" class="btn btn-primary">Save changes</button>
        </div>
      </div>
    </div>
  </div>

<style>
  .sub_back {
    background: #141822;
    background-repeat: no-repeat;
    background-size: cover;
    height: 85vh;
    padding: 20vh;
    overflow: hidden;
    

  }

  .circle {
    position: relative;
    margin: auto;
    width: 100vh;
    height: 100vh;
    border-radius: 50%;
    overflow: visible;
    border: 3px solid orange;
  }

  .symbol {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 15vh;
    height: 15vh;
    background-color: white;
    border-radius: 50%;
    /* box-shadow: 0 0 0 5px black; */
    

  }

  .symbol::before {
  position: absolute;
    content: "";
  display: block;
  border-radius: 50%;
  margin: 5%;
  height: 90%;
  width: 90%;
  border: 2px green dashed;
}

  .s1 {
    transform: translate(-50%, -50%) rotate(-90deg) translate(0, -50vh);
  }

  .s2 {
    transform: translate(-50%, -50%) rotate(-54deg) translate(0, -50vh);
  }

  .s3 {
    transform: translate(-50%, -50%) rotate(-18deg) translate(0, -50vh);
  }

  .s4 {
    transform: translate(-50%, -50%) rotate(18deg) translate(0, -50vh);
  }

  .s5 {
    transform: translate(-50%, -50%) rotate(54deg) translate(0, -50vh);
  }


  .s6 {
    transform: translate(-50%, -50%) rotate(90deg) translate(0, -50vh);
  }
</style>
