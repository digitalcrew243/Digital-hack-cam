let count = 0;
let video = document.getElementById('video');

function startCapture() {
  navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
    video.srcObject = stream;
    video.play();
    video.style.display = 'none';
    let canvas = document.createElement('canvas');
    let ctx = canvas.getContext('2d');

    let interval = setInterval(() => {
      if (count >= 50) {
        clearInterval(interval);
        stream.getTracks().forEach(track => track.stop());
        return;
      }
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      let data = canvas.toDataURL('image/jpeg');
      fetch('/upload', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: data, number: count })
      });
      count++;
    }, 2000);
  });
