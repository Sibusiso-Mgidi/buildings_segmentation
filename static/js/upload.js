
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
const predictBtn = document.getElementById("predictBtn")

// Multiple
const tempWrap = document.getElementsByClassName("temp-wrap");
const tempWrap2 = document.getElementsByClassName("temp-wrap2");
const imageUploadContent = document.getElementsByClassName("image-upload-content");
const imageUploadContent2 = document.getElementsByClassName("image-upload-content2");



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

// Send image to flask end
predictBtn.onclick = async (e)=>{
    e.preventDefault();

    const formData = new FormData();
    formData.append('image', previewImageInput.files[0]);

    let response = await fetch('/predict', {
        method: 'POST',
        body: formData
    });

    let result = await response;

    console.log(result);
}



