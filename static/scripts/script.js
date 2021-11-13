var checks = $(".form-checks")

var webp2png = ["<input class='check-box' type='checkbox' name='webp2png' id='png_box'>", "<label class='check-label' for='png_box'>To PNG</label>"]
var webp2jpg = ["<input class='check-box' type='checkbox' name='webp2jpg' id='jpg_box'>", "<label class='check-label' for='jpg_box'>To JPG</label>"]
var jpg2png = ["<input class='check-box' type='checkbox' name='jpg2png' id='png_box'>", "<label class='check-label' for='png_box'>To PNG</label>"]
var png2jpg = ["<input class='check-box' type='checkbox' name='png2jpg' id='jpb_box'>", "<label class='check-label' for='jpb_box'>To JPG</label>"]
var png2webp = ["<input class='check-box' type='checkbox' name='png2webp' id='webp_box'>", "<label class='check-label' for='webp_box'>To WEBP</label>"]
var jpg2webp = ["<input class='check-box' type='checkbox' name='jpg2webp' id='webp_box'>", "<label class='check-label' for='webp_box'>To WEBP</label>"]
var img2pdf = ["<input class='check-box' type='checkbox' name='img2pdf' id='pdf_box'>", "<label class='check-label' for='pdf_box'>To PDF</label>"]
var pdf2jpg = ["<input class='check-box' type='checkbox' name='pdf2jpg' id='pdf_box'>", "<label class='check-label' for='pdf_box'>To JPG</label>"]
var pdf2mp3 = ["<input class='check-box' type='checkbox' name='pdf2mp3' id='mp3'>", "<label class='check-label' for='mp3'>To MP3</label>"]
var docx2pdf = ["<input class='check-box' type='checkbox' name='docx' id='docx_box'>", "<label class='check-label' for='docx_box'>To DOCX</label>"]
var mp42mkv = ["<input class='check-box' type='checkbox' name='mp42mkv' id='mp4_box'>", "<label class='check-label' for='mp4_box'>To MP4</label>"]
var mkv2mp4 = ["<input class='check-box' type='checkbox' name='mkv2mp4' id='mkv_box'>", "<label class='check-label' for='mkv_box'>To MKV</label>"]

function getFileData(myFile) {
    var file = myFile.files[0]
    var filename = file.name
    var o_name = filename.split(".")[0]
    var file_extension = filename.split('.').pop().toLowerCase()

    var size = file.size;
    var fSExt = new Array('Bytes', 'KB', 'MB', 'GB'),
    i=0;while(size>900){size/=1024;i++;}
    var exactSize = (Math.round(size*100)/100)+' '+fSExt[i];
    
    $(".noselect").css('display', 'none')
    $(".form-container").css('display', 'flex')
    $(".file-name").html(filename)
    $(".file-size").html(exactSize)

    if(file_extension==="png") {
        checks.append(png2jpg, png2webp, img2pdf)
    }
    else if(file_extension==="jpg" || file_extension==="jpeg") {
        checks.append(jpg2png, jpg2webp, img2pdf)
    }
    else if(file_extension==="webp") {
        checks.append(webp2png, webp2jpg, img2pdf)
    }
    else if(file_extension==="pdf") {
        checks.append(pdf2jpg, pdf2mp3)
    }
    else if(file_extension==="docx" || file_extension==="doc") {
        checks.append(docx2pdf)
    }
    else if(file_extension==="mp4") {
        checks.append(mp42mkv)
    }
    else if(file_extension==="mkv") {
        checks.append(mkv2mp4)
    }
}

$(".final-submit").click(function() {
    $(".form-container").css('display', 'none')
    $(".form-container-2").css('display', 'flex')
})

$(".back").click(function(){
    location.reload();
});