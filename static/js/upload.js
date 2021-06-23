
// =============== GRAB ELEMENTS =============== 
// Preview Image
const prevUploadBtn = document.getElementById("prevUploadBtn");
const previewImageInput = document.getElementById("previewImageInput");
const previewImage = document.getElementById("previewImage");
const previewImage2 = document.getElementById("previewImage2");

// Mask Image
const maskUploadBtn = document.getElementById("maskUploadBtn");
const maskImageInput = document.getElementById("maskImageInput");
const maskImage = document.getElementById("maskImage");
const maskImage2 = document.getElementById("maskImage2");

// Predition
const predictBtn = document.getElementById("predictBtn");
const predictImage = document.getElementById("predictionImage1");
const predictImage2 = document.getElementById("predictionImage2");

// Multiple
const tempWrap = document.getElementsByClassName("temp-wrap");
const tempWrap2 = document.getElementsByClassName("temp-wrap2");
const imageUploadContent = document.getElementsByClassName("image-upload-content");
const imageUploadContent2 = document.getElementsByClassName("image-upload-content2");

// Predition output (IOU)
const predictOut = document.getElementById("pred-out-1")
const predictOut2 = document.getElementById("pred-out-2")


// =============== METHODS =============== 

// Button Eventlistners
prevUploadBtn.addEventListener("click", function (){

    previewImageInput.click();

});
maskUploadBtn.addEventListener("click", function (){

    maskImageInput.click();

});

// Image Input Eventlisteners
previewImageInput.addEventListener("change",function (){

    const image = previewImageInput.files[0]; 
    // console.log(image)

    if (image) {

        //Read File
        const fileReader = new FileReader();

        fileReader.addEventListener("load", function () {

            tempWrap[0].style.display ="none";
            tempWrap2[0].style.display ="none";

            previewImage.setAttribute("src", this.result);
            previewImage2.setAttribute("src",this.result)
            imageUploadContent[0].style.display = "block";
            imageUploadContent2[0].style.display = "block";
            

        });
        fileReader.readAsDataURL(image);

    }

});
maskImageInput.addEventListener("change",function (){

    const image = maskImageInput.files[0]; 
    // console.log(image)

    if (image) {

        //Read File
        const fileReader = new FileReader();

        fileReader.addEventListener("load", function () {
            tempWrap[1].style.display ="none";
            tempWrap2[1].style.display ="none";

            maskImage.setAttribute("src", this.result);
            maskImage2.setAttribute("src", this.result);
            imageUploadContent[1].style.display = "block";
            imageUploadContent2[1].style.display = "block";
            

        });
        fileReader.readAsDataURL(image);

    }

});

// Send image and mask to Flask server and display results
predictBtn.onclick = async (e)=>{
    e.preventDefault();

    if(!previewImageInput.files[0]){
        alert('Please supply Image');
        return
    }

    if(!maskImageInput.files[0]){
        alert('Please supply Mask');
        return
    }

    const formData = new FormData();
    formData.append('image', previewImageInput.files[0]);
    formData.append('mask', maskImageInput.files[0]);

    

    let response = await fetch('/predict', {
        method: 'POST',
        body: formData
    });

    let result = await response;
    result.json().then( data =>{

        res_img_1 = data['pred_image_1'];
        res_img_2 = data['pred_image_2'];
        pred_1 = data['iou_1'];
        pred_2 = data['iou_2'];

        res_img_1 = 'data:image/png;base64,'+res_img_1;
        res_img_2 = 'data:image/png;base64,'+res_img_2;
      
        tempWrap[2].style.display ="none";
        tempWrap2[2].style.display ="none";

        predictImage.setAttribute("src",res_img_1);
        predictImage2.setAttribute("src",res_img_2);

        imageUploadContent[2].style.display = "block";
        imageUploadContent2[2].style.display = "block";

        predictOut.innerText = "Prediction: "+pred_1;
        predictOut2.innerText = "Prediction: "+pred_2;


    }).catch(error =>{
        console.log(error)
    })

}



