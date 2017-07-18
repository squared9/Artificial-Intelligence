// Mimic Me!
// Fun game where you need to express emojis being displayed

// --- Affectiva setup ---

// The affdex SDK Needs to create video and canvas elements in the DOM
var divRoot = $("#camera")[0];  // div node where we want to add these elements
var width = 640, height = 480;  // camera image size
var faceMode = affdex.FaceDetectorMode.LARGE_FACES;  // face mode parameter

// Initialize an Affectiva CameraDetector object
var detector = new affdex.CameraDetector(divRoot, width, height, faceMode);

// Enable detection of all Expressions, Emotions and Emojis classifiers.
detector.detectAllEmotions();
detector.detectAllExpressions();
detector.detectAllEmojis();
detector.detectAllAppearance();

// --- Utility values and functions ---

// Unicode values for all emojis Affectiva can detect
var emojis = [ 128528, 9786, 128515, 128524, 128527, 128521, 128535, 128539, 128540, 128542, 128545, 128563, 128561 ];

// Update target emoji being displayed by supplying a unicode value
function setTargetEmoji(code) {
  $("#target").html("&#" + code + ";");
}

// Convert a special character to its unicode value (can be 1 or 2 units long)
function toUnicode(c) {
  if(c.length == 1)
    return c.charCodeAt(0);
  return ((((c.charCodeAt(0) - 0xD800) * 0x400) + (c.charCodeAt(1) - 0xDC00) + 0x10000));
}

// Update score being displayed
function setScore(correct, total) {
  $("#score").html("Score: " + correct + " / " + total);
}

// Display log messages and tracking results
function log(node_name, msg) {
  $(node_name).append("<span>" + msg + "</span><br />")
}

// --- Callback functions ---

// Start button
function onStart() {
  if (detector && !detector.isRunning) {
    $("#logs").html("");  // clear out previous log
    detector.start();  // start detector
  }
  log('#logs', "Start button pressed");
}

// Stop button
function onStop() {
  log('#logs', "Stop button pressed");
  if (detector && detector.isRunning) {
    detector.removeEventListener();
    detector.stop();  // stop detector
  }
};

// Reset button
function onReset() {
  log('#logs', "Reset button pressed");
  if (detector && detector.isRunning) {
    detector.reset();
  }
  $('#results').html("");  // clear out results
  $("#logs").html("");  // clear out previous log

  reinitialize();
};

// Add a callback to notify when camera access is allowed
detector.addEventListener("onWebcamConnectSuccess", function() {
  log('#logs', "Webcam access allowed");
});

// Add a callback to notify when camera access is denied
detector.addEventListener("onWebcamConnectFailure", function() {
  log('#logs', "webcam denied");
  console.log("Webcam access denied");
});

// Add a callback to notify when detector is stopped
detector.addEventListener("onStopSuccess", function() {
  log('#logs', "The detector reports stopped");
  $("#results").html("");
});

// Add a callback to notify when the detector is initialized and ready for running
detector.addEventListener("onInitializeSuccess", function() {
  log('#logs', "The detector reports initialized");
  //Display canvas instead of video feed because we want to draw the feature points on it
  $("#face_video_canvas").css("display", "block");
  $("#face_video").css("display", "none");

  reinitialize();
});

// Add a callback to receive the results from processing an image
// NOTE: The faces object contains a list of the faces detected in the image,
//   probabilities for different expressions, emotions and appearance metrics
detector.addEventListener("onImageResultsSuccess", function(faces, image, timestamp) {
  var canvas = $('#face_video_canvas')[0];
  if (!canvas)
    return;

  // Report how many faces were found
  $('#results').html("");
  log('#results', "Timestamp: " + timestamp.toFixed(2));
  log('#results', "Number of faces found: " + faces.length);
  if (faces.length > 0) {
    // Report desired metrics
    log('#results', "Appearance: " + JSON.stringify(faces[0].appearance));
    log('#results', "Emotions: " + JSON.stringify(faces[0].emotions, function(key, val) {
      return val.toFixed ? Number(val.toFixed(0)) : val;
    }));
    log('#results', "Expressions: " + JSON.stringify(faces[0].expressions, function(key, val) {
      return val.toFixed ? Number(val.toFixed(0)) : val;
    }));
    log('#results', "Emoji: " + faces[0].emojis.dominantEmoji);

    // Call functions to draw feature points and dominant emoji (for the first face only)
    drawFeaturePoints(canvas, image, faces[0]);
    drawEmoji(canvas, image, faces[0]);
    advanceGame(canvas, image, faces[0]);
  }
});


// --- Custom functions ---

// Draw the detected facial feature points on the image
function drawFeaturePoints(canvas, img, face) {
  // Obtain a 2D context object to draw on the canvas
  var ctx = canvas.getContext('2d');

  ctx.fillStyle = "white";
  ctx.lineWidth = 1;
  ctx.strokeStyle = "orange";
  var radius = 3;

  // Loop over each feature point in the face
  for (var id in face.featurePoints) {
    var featurePoint = face.featurePoints[id];
    ctx.beginPath();
    ctx.arc(featurePoint.x, featurePoint.y, radius, 0, 2 * Math.PI, false);
    ctx.fill();
    ctx.stroke();
  }
}

// Draw the dominant emoji on the image
function drawEmoji(canvas, img, face) {
  // Obtain a 2D context object to draw on the canvas
  var ctx = canvas.getContext('2d');

  // get top-right coordinate
  var x = -100000;
  var y = 100000;
  for (var id in face.featurePoints) {
    var featurePoint = face.featurePoints[id];
    if (x < featurePoint.x)
      x = featurePoint.x;
    if (y > featurePoint.y)
      y = featurePoint.y;
  }

  x += 20;
  y -= 20;

  ctx.fillStyle = "yellow";
  ctx.font = "bold 128px Arial";
  var emoji = face.emojis.dominantEmoji;
  ctx.fillText(emoji, x, y);
}

// TODO: Define any variables and functions to implement the Mimic Me! game mechanics

function reinitialize() {
  // Simple linear finite state machine
  // states:
  // 0 - init
  // 1 - Get Ready animation
  // 2 - Mimicking
  // 3 - Sucess
  // 4 - Failure
  // 0->1->2->3->2->4->2->... sequence
  state = 0;
  emoji_to_do = null;
  frame = 0;
  animation_start_frame = -1;
  animation_duration = -1;
  is_sensing = false;
  score = 0;
  attempts = 0;
  sensing_frames = 100;
  setScore(0,0);
  setTargetEmoji(63);
}

function advanceGame(canvas, img, face) {
  // Obtain a 2D context object to draw on the canvas
  log("advancing game");
  frame += 1;
  var ctx = canvas.getContext('2d');

  if (state == 0) {
    //
    // Init
    //
    // log("#logs", "state 0 -- init");
    state = 1;
  } else if (state == 1) {
    //
    // Get Ready
    //
    // log("#logs", "state 1 -- get ready");
    if (animation_duration < 0) {
      animation_duration = 30;
      animation_start_frame = frame;
    } else if (animation_duration == 0) {
      // next state
      state = 2;
      animation_start_frame = -1;
      return;
    }
    ctx.fillStyle = "green";
    ctx.font = "bold 64px Arial";
    ctx.fillText("GET READY!", 30 + Math.random(5), 100 + Math.random(5));
    animation_duration--;
  } else if (state == 2) {
    //
    // Mimic Me!
    //
    // log("#logs", "state 2 -- mimic me");
    if (animation_start_frame < 0) {
      emoji_to_do = emojis[Math.floor(Math.random() * emojis.length)];
      setTargetEmoji(emoji_to_do);
      animation_start_frame = frame;
      animation_duration = -1;
      is_sensing = false;
    }

    time_to_go = sensing_frames - frame + animation_start_frame;
    if (time_to_go <= 0) {
      state = 4;
      animation_duration = -1;
      return;
    }

    ctx.fillStyle = "blue";
    ctx.font = "bold 64px Arial";
    ctx.fillText(time_to_go, 30, 100);

    if (toUnicode(face.emojis.dominantEmoji) == emoji_to_do) {
      if (is_sensing) {
        if (animation_duration == 0) {
          state = 3;
          animation_duration = -1;
          return;
        }
        animation_duration--;
      } else {
        is_sensing = true;
        animation_duration = 3;
      }
    } else {
      is_sensing = false;
      animation_duration = -1;
    }
  } else if (state == 3) {
    //
    // Success
    //
    // log("#logs", "state 3 -- success");
    if (animation_duration < 0) {
      animation_duration = 30;
      animation_start_frame = frame;
      score += 1;
      attempts += 1;
      setScore(score, attempts);
    } else if (animation_duration == 0) {
      // next state
      state = 2;
      animation_start_frame = -1;
      return;
    }
    ctx.fillStyle = "red";
    ctx.font = "bold 96px Arial";
    ctx.fillText("AWESOME!", 30 + Math.random(5), 100 + Math.random(5));
    animation_duration--;
  } else if (state == 4) {
    //
    // Failure
    //
    // log("#logs", "state 4 -- fail");
    if (animation_duration < 0) {
      animation_duration = 30;
      animation_start_frame = frame;
      attempts += 1;
      setScore(score, attempts);
    } else if (animation_duration == 0) {
      // next state
      state = 2;
      animation_start_frame = -1;
      return;
    }
    ctx.fillStyle = "black";
    ctx.font = "bold 96px Arial";
    ctx.fillText("FAIL!", 30 + Math.random(5), 100 + Math.random(5));
    animation_duration--;
  }
}

// NOTE:
// - Remember to call your update function from the "onImageResultsSuccess" event handler above
// - You can use setTargetEmoji() and setScore() functions to update the respective elements
// - You will have to pass in emojis as unicode values, e.g. setTargetEmoji(128578) for a simple smiley
// - Unicode values for all emojis recognized by Affectiva are provided above in the list 'emojis'
// - To check for a match, you can convert the dominant emoji to unicode using the toUnicode() function

// Optional:
// - Define an initialization/reset function, and call it from the "onInitializeSuccess" event handler above
// - Define a game reset function (same as init?), and call it from the onReset() function above

// <your code here>
