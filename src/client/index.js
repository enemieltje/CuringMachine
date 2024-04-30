let previewActive = false

function testButton() {
    console.log("test!")
}

function toggleButton() {
    const button = document.getElementById('toggleButton')
    if (previewActive){
        fetch('/button/stopcam')

        const img = document.getElementById('stream')
        img.remove()
        button.innerHTML = 'Start Preview'
    }else{
        fetch('/button/startcam').then(()=>{

            const img = document.createElement('img')
            img.setAttribute('id', 'stream')
            img.setAttribute('src', 'stream.mjpg')
            img.setAttribute('width', '640')
            img.setAttribute('height', '480')
            img.setAttribute('alt', 'Camera Offline')

            const div = document.getElementById('streamdiv')
            div.appendChild(img)
        })
        button.innerHTML = 'Stop Preview'
    }
    previewActive = !previewActive
}

function showcaseButton() {
    fetch('/button/showcase')
}

function pictureButton() {
    redirect('/button/picture')
}

function redirect(url){
    console.debug("redirecting to:", window.location.host + url)
    window.location.href = 'http://' + window.location.host + url
}
