window.AudioContext = window.AudioContext || window.webkitAudioContext;

var URL = "https://siroop.recapp.ch:10002/asr/";

var audioContext = new AudioContext();
var audioInput = null,
    realAudioInput = null,
    inputPoint = null,
    audioRecorder = null;
var rafID = null;
var analyserContext = null;
var canvasWidth, canvasHeight;
var recIndex = 0;
var productList = null;
var productData = [];
var init = true;
var currentVue = null;

// DOM Loaded ( we have to be sure that all elements are available )
document.addEventListener('DOMContentLoaded', function () {
    var recordingButton = document.getElementById('btn-record');
    var form_input_text = document.getElementById('form_text_input');

    initVue();

    recordingButton.addEventListener('mousedown', function (ev) {
        startRecording(ev);
        updateStatus("Listening... ");
    });

    form_input_text.addEventListener('submit', function (ev) {
        event.preventDefault();
        var statusS = document.getElementById("search_input");
        executeSearch(statusS.value);
    });

    recordingButton.addEventListener('mouseup', function (ev) {
        stopRecording(ev);
    });
});

function initVue() {
    currentVue = new Vue({
        el: '#productList',
        data: {
            products: productList
        },
        methods: {
            updateAll: function (data) {
                console.log('update all method 1', data);
                this.products = data;
            }
        }
    });
}

function getProducts(searchTerm, cb) {
    console.log('get products');
    $.get({
        url: 'http://www-explorer.pthor.ch/elastic/all_products_spryker_read/_search?q=' + searchTerm + '&size=12',
        success: function (result) {
            productList = result.hits.hits;
            cb(productList);
        },
        error: function (err) {
            console.log('error from api', err);
        }
    });
}

function sendBlob(blob) {

    updateStatus("Loading... ");

    var fd = new FormData();
    fd.append('fname', 'test.wav');
    fd.append('data', blob);

    $.post({
        url: URL,
        data: blob,
        success: function (result) {
            console.log(result.data);
            executeSearch(result.data[0]['textParsed']);
        },
        processData: false,
        contentType: false
    });

}

function updateStatus(status) {
    var statusS = document.getElementById("search_input");
    statusS.value = status;

    console.log('updating status....');

}

function executeSearch(value) {
    var fieldInput = document.getElementById("search_input");
    fieldInput.value = value;

    getProducts(value, function(products) {
        currentVue.updateAll(products);
    });
}

function startRecording(event) {
    event.preventDefault();
    var el = event.currentTarget;
    var searchField = document.getElementById('form_text_input');
    el.classList.add("recording");
    searchField.classList.add("recording");
    audioRecorder.clear();
    audioRecorder.record();
}

function stopRecording(ev) {
    event.preventDefault();
    var el = event.currentTarget;
    var searchField = document.getElementById('form_text_input');
    el.classList.remove("recording");
    searchField.classList.remove("recording");
    audioRecorder.stop();
    audioRecorder.getBuffers(gotBuffers);
}

function gotBuffers(buffers) {
    var canvas = document.getElementById("wavedisplay");

    //drawBuffer(canvas.width, canvas.height, canvas.getContext('2d'), buffers[0]);

    // the ONLY time gotBuffers is called is right after a new recording is completed -
    // so here's where we should set up the download.
    audioRecorder.exportMonoWAV(sendBlob);
    //apiaiSend();
}

function gotStream(stream) {
    inputPoint = audioContext.createGain();

    // Create an AudioNode from the stream.
    realAudioInput = audioContext.createMediaStreamSource(stream);
    audioInput = realAudioInput;
    audioInput.connect(inputPoint);

//    audioInput = convertToMono( input );

    analyserNode = audioContext.createAnalyser();
    analyserNode.fftSize = 2048;
    inputPoint.connect(analyserNode);

    audioRecorder = new Recorder(inputPoint);

    zeroGain = audioContext.createGain();
    zeroGain.gain.value = 0.0;
    inputPoint.connect(zeroGain);
    zeroGain.connect(audioContext.destination);
    //updateAnalysers();
}

function initAudio() {
    if (!navigator.getUserMedia)
        navigator.getUserMedia = navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
    if (!navigator.cancelAnimationFrame)
        navigator.cancelAnimationFrame = navigator.webkitCancelAnimationFrame || navigator.mozCancelAnimationFrame;
    if (!navigator.requestAnimationFrame)
        navigator.requestAnimationFrame = navigator.webkitRequestAnimationFrame || navigator.mozRequestAnimationFrame;

    navigator.getUserMedia(
        {
            "audio": {
                "mandatory": {
                    "googEchoCancellation": "false",
                    "googAutoGainControl": "false",
                    "googNoiseSuppression": "false",
                    "googHighpassFilter": "false"
                },
                "optional": []
            },
        }, gotStream, function (e) {
            alert('Error getting audio');
            console.log(e);
        });
}

window.addEventListener('load', initAudio);