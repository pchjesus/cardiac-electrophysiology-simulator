/*
========================================

Cardiac Electrophysiology Simulator

Sinus Rhythm ECG Engine v1.5

FINAL UI PATCH

Changes:

- Heart Rate slider: 30–180 bpm
- 80 bpm = Normal speed reference
- 30 bpm = minimum animation speed
- 180 bpm = maximum animation speed
- Normal Range: 60–100 bpm
- Bradycardia <60
- Normal Sinus Rhythm 60–100
- Tachycardia >100
- Overall animation speed reduced by 20%
- ECG interpretation stays on one line

========================================
*/



// ===============================
// STATE
// ===============================

const heartState = {

    playing:false,

    ecgTime:0,

    lastTimestamp:null,

    currentStep:-1,

    currentECGEvent:null,

    sweepPosition:0

};



// ===============================
// INTERNAL SPEED
// ===============================

/*

Internal speed remains separate
from the user-facing Heart Rate.

Heart Rate is converted into
an animation speed.

80 bpm = 1.0 reference speed.

30 bpm = minimum speed.

180 bpm = maximum speed.

*/

let animationSpeed = 1.0;



// ===============================
// HEART RATE
// ===============================

let heartRate = 80;



// ===============================
// SPEED SETTINGS
// ===============================

/*

The previous version used
BASE_SPEED_FACTOR = 0.5.

This version reduces the overall
animation speed by another 20%.

0.5 × 0.8 = 0.4

Therefore all animation systems
using this factor are slowed
by 20% relative to the previous
version.

*/

const BASE_SPEED_FACTOR = 0.4;



// Minimum internal animation speed.

const MIN_ANIMATION_SPEED = 0.15;



// Maximum internal animation speed.

const MAX_ANIMATION_SPEED = 2.0;



// Normal reference speed.

const NORMAL_ANIMATION_SPEED = 1.0;



// ===============================
// ECG SETTINGS
// ===============================

const baseCycleLength =
60000 / 72;


// ===============================
// ECG MEASUREMENT MODEL
// ===============================

/*

Measurement values are derived from the
current simulated ECG timing model.
They are educational simulator values,
not measurements from a real patient ECG.

*/

const ECG_MEASUREMENT_TIMING = {

    pStart:80,

    qrsStart:300,

    qrsEnd:380,

    tEnd:680

};



const sweepDuration = 3000;



// ===============================
// DOM
// ===============================

const canvas =
document.getElementById(
    "ecgCanvas"
);


const ctx =
canvas.getContext("2d");



const phaseTitle =
document.getElementById(
    "phaseTitle"
);


const phaseDescription =
document.getElementById(
    "phaseDescription"
);


const phaseECG =
document.getElementById(
    "phaseECG"
);


const rhythmStatus =
document.getElementById(
    "rhythmStatus"
);


const heartRateDisplay =
document.getElementById(
    "heartRateDisplay"
);


const heartRateSlider =
document.getElementById(
    "heartRateSlider"
);


const heartRateValue =
document.getElementById(
    "heartRateValue"
);


const measurementHeartRate =
document.getElementById(
    "measurementHeartRate"
);


const measurementRR =
document.getElementById(
    "measurementRR"
);


const measurementPR =
document.getElementById(
    "measurementPR"
);


const measurementQRS =
document.getElementById(
    "measurementQRS"
);


const measurementQT =
document.getElementById(
    "measurementQT"
);


const measurementQTc =
document.getElementById(
    "measurementQTc"
);


const playBtn =
document.getElementById(
    "playBtn"
);


const pauseBtn =
document.getElementById(
    "pauseBtn"
);


const resetBtn =
document.getElementById(
    "resetBtn"
);


const slider =
document.getElementById(
    "timeSlider"
);



const atriaRegion =
document.getElementById(
    "atriaRegion"
);


const ventricleRegion =
document.getElementById(
    "ventricleRegion"
);


const conductionPulse =
document.getElementById(
    "conductionPulse"
);

const conductionPulseR =
document.getElementById(
    "conductionPulseR"
);

const conductionPulseL =
document.getElementById(
    "conductionPulseL"
);


const ecgEventIndicator =
document.getElementById(
    "ecgEventIndicator"
);


const eventSyncStatus =
document.getElementById(
    "eventSyncStatus"
);


const eventFlowItems =
document.querySelectorAll(
    ".event-item[data-conduction]"
);


const ecgComponentItems =
document.querySelectorAll(
    ".ecg-item[data-ecg-component]"
);

const ecgExplanationTitle =
document.getElementById(
    "ecgExplanationTitle"
);

const ecgExplanationText =
document.getElementById(
    "ecgExplanationText"
);

const ecgExplanationLink =
document.getElementById(
    "ecgExplanationLink"
);



// ===============================
// ECG DATA
// ===============================

let ecgPoints = [];



// ===============================
// CONDUCTION STEPS
// ===============================

const conductionSteps = [

    {

        id:"SA",

        start:0,

        end:130,

        title:
        "SA Node Activation",

        description:
        "The sinoatrial (SA) node initiates the electrical impulse. Atrial depolarization produces the P wave.",

        ecg:
        "P Wave"

    },


    {

        id:"AV",

        start:130,

        end:250,

        title:
        "AV Node Delay",

        description:
        "The impulse reaches the atrioventricular (AV) node. Conduction slows briefly, contributing to the PR interval.",

        ecg:
        "PR Interval"

    },


    {

        id:"His",

        start:250,

        end:305,

        title:
        "His Bundle Conduction",

        description:
        "The electrical impulse travels through the His bundle toward the ventricular conduction system.",

        ecg:
        "PR Interval"

    },


    {

        id:"Branches",

        start:305,

        end:380,

        title:
        "Bundle Branch Activation",

        description:
        "The impulse rapidly travels through the right and left bundle branches toward the Purkinje fibers.",

        ecg:
        "QRS Complex"

    },


    {

        id:"Purkinje",

        start:380,

        end:450,

        title:
        "Purkinje Activation",

        description:
        "Purkinje fibers rapidly distribute the impulse throughout the ventricles, producing ventricular depolarization and the QRS complex.",

        ecg:
        "QRS Complex"

    },


    {

        id:"Recovery",

        start:450,

        end:700,

        title:
        "Ventricular Recovery",

        description:
        "The ventricles recover electrically. The ST segment precedes ventricular repolarization represented by the T wave.",

        ecg:
        "ST / T Wave"

    }

];


// ===============================
// INTERACTIVE ECG EXPLANATION
// ===============================

const ecgComponentExplanations = {

    P: {
        title: "P Wave",
        text: "Represents atrial depolarization. In this simulator, it follows SA node activation and corresponds to electrical activation spreading through the atria.",
        link: "SA Node → Atria"
    },

    PR: {
        title: "PR Interval",
        text: "Represents the time from the start of atrial depolarization to the start of ventricular depolarization. The AV node contributes to the conduction delay before the impulse continues through the His-Purkinje system.",
        link: "AV Node → His Bundle"
    },

    QRS: {
        title: "QRS Complex",
        text: "Represents ventricular depolarization. The impulse travels through the His bundle, right and left bundle branches, and Purkinje fibers to activate the ventricles.",
        link: "His → RBB/LBB → Purkinje"
    },

    ST: {
        title: "ST Segment",
        text: "Follows ventricular depolarization in the simulator's simplified ECG model. It represents the early ventricular recovery portion before the T wave.",
        link: "Ventricular recovery"
    },

    T: {
        title: "T Wave",
        text: "Represents ventricular repolarization, the electrical recovery of the ventricles after depolarization.",
        link: "Ventricular repolarization"
    }

};

let selectedECGComponent = null;

function selectECGComponent(componentId){

    const explanation =
    ecgComponentExplanations[componentId];

    if(!explanation){
        return;
    }

    selectedECGComponent = componentId;

    ecgComponentItems.forEach(
        item => {

            item.classList.toggle(
                "ecg-selected",
                item.dataset.ecgComponent === componentId
            );

        }
    );

    ecgExplanationTitle.textContent =
    explanation.title;

    ecgExplanationText.textContent =
    explanation.text;

    ecgExplanationLink.textContent =
    explanation.link;

}

function syncECGExplanationToEvent(eventId){

    const componentId =
    ecgComponentExplanations[eventId]
        ? eventId
        : null;

    if(componentId){

        selectECGComponent(componentId);
        return;

    }

    selectedECGComponent = null;

    ecgComponentItems.forEach(
        item => item.classList.remove(
            "ecg-selected"
        )
    );

    ecgExplanationTitle.textContent =
    "Baseline";

    ecgExplanationText.textContent =
    "No major ECG deflection is represented in this portion of the cycle. The simulator treats it as the resting baseline between ECG events.";

    ecgExplanationLink.textContent =
    "Resting baseline";

}

{
    ecgComponentItems.forEach(
        item => {

            item.addEventListener(
                "click",
                () => selectECGComponent(
                    item.dataset.ecgComponent
                )
            );

        }
    );
}

// ===============================
// ECG EVENT MODEL
// ===============================

const ecgEvents = [

    {
        id:"Baseline",
        start:0,
        end:80,
        label:"Baseline"
    },

    {
        id:"P",
        start:80,
        end:160,
        label:"P Wave"
    },

    {
        id:"PR",
        start:160,
        end:300,
        label:"PR Interval"
    },

    {
        id:"QRS",
        start:300,
        end:380,
        label:"QRS Complex"
    },

    {
        id:"ST",
        start:380,
        end:500,
        label:"ST Segment"
    },

    {
        id:"T",
        start:500,
        end:680,
        label:"T Wave"
    },

    {
        id:"Baseline",
        start:680,
        end:baseCycleLength,
        label:"Baseline"
    }

];



// ===============================
// HEART RATE → SPEED
// ===============================

function heartRateToSpeed(
    hr
){

    /*

    30 bpm
    → minimum animation speed

    80 bpm
    → normal animation speed

    180 bpm
    → maximum animation speed

    The minimum is deliberately
    NOT zero, so 30 bpm does not
    stop the simulation.

    */


    if(hr <= 80){

        const progress =

        (
            hr - 30
        ) / 50;



        return (

            MIN_ANIMATION_SPEED

            +

            progress *

            (

                NORMAL_ANIMATION_SPEED
                -
                MIN_ANIMATION_SPEED

            )

        );

    }



    const progress =

    (

        hr - 80

    ) / 100;



    return (

        NORMAL_ANIMATION_SPEED

        +

        progress *

        (

            MAX_ANIMATION_SPEED
            -
            NORMAL_ANIMATION_SPEED

        )

    );

}



// ===============================
// UPDATE HEART RATE UI
// ===============================

function updateHeartRateUI(){



    heartRateDisplay.textContent =

        "Heart Rate : " +

        heartRate +

        " bpm";



    heartRateValue.textContent =

        heartRate +

        " bpm";



    // =========================
    // RHYTHM STATUS
    // =========================

    if(

        heartRate < 60

    ){

        rhythmStatus.textContent =
        "Sinus Bradycardia";

    }


    else if(

        heartRate <= 100

    ){

        rhythmStatus.textContent =
        "Normal Sinus Rhythm";

    }


    else{

        rhythmStatus.textContent =
        "Sinus Tachycardia";

    }



    // =========================
    // INTERNAL SPEED
    // =========================

    animationSpeed =

        heartRateToSpeed(
            heartRate
        );


    updateECGMeasurements();

}



// ===============================
// ECG MEASUREMENTS
// ===============================

function getECGMeasurements(){

    const rrInterval =
    60000 / heartRate;


    const prInterval =
    ECG_MEASUREMENT_TIMING.qrsStart
    -
    ECG_MEASUREMENT_TIMING.pStart;


    const qrsDuration =
    ECG_MEASUREMENT_TIMING.qrsEnd
    -
    ECG_MEASUREMENT_TIMING.qrsStart;


    const qtInterval =
    ECG_MEASUREMENT_TIMING.tEnd
    -
    ECG_MEASUREMENT_TIMING.qrsStart;


    // Bazett correction. RR is converted to seconds.
    const qtc =
    qtInterval /
    Math.sqrt(rrInterval / 1000);


    return {

        heartRate:heartRate,

        rrInterval:rrInterval,

        prInterval:prInterval,

        qrsDuration:qrsDuration,

        qtInterval:qtInterval,

        qtc:qtc

    };

}


function updateECGMeasurements(){

    const measurements =
    getECGMeasurements();


    measurementHeartRate.textContent =
    measurements.heartRate + " bpm";


    measurementRR.textContent =
    Math.round(measurements.rrInterval) + " ms";


    measurementPR.textContent =
    measurements.prInterval + " ms";


    measurementQRS.textContent =
    measurements.qrsDuration + " ms";


    measurementQT.textContent =
    measurements.qtInterval + " ms";


    measurementQTc.textContent =
    Math.round(measurements.qtc) + " ms";

}


// ===============================
// ECG MODEL
// ===============================

function ecgValue(t){



    if(t < 0){

        return 0;

    }



    t =

    t %

    baseCycleLength;



    let value = 0;



    // =========================
    // P WAVE
    // =========================

    if(

        t >= 80 &&

        t <= 160

    ){

        const x =

        (t - 80) / 80;



        value =

        Math.sin(

            Math.PI * x

        ) * 25;

    }



    // =========================
    // QRS
    // =========================

    if(

        t >= 300 &&

        t <= 380

    ){

        const x =

        (t - 300) / 80;



        if(x < 0.25){

            value =

            -25 *

            Math.sin(

                Math.PI *
                x /
                0.25

            );

        }


        else if(x < 0.55){

            value =

            120 *

            Math.sin(

                Math.PI *

                (x - 0.25) /

                0.3

            );

        }


        else{

            value =

            -40 *

            Math.sin(

                Math.PI *

                (x - 0.55) /

                0.45

            );

        }

    }



    // =========================
    // ST
    // =========================

    if(

        t > 380 &&

        t < 500

    ){

        value = 0;

    }



    // =========================
    // T WAVE
    // =========================

    if(

        t >= 500 &&

        t <= 680

    ){

        const x =

        (t - 500) / 180;



        value =

        Math.sin(

            Math.PI * x

        ) * 35;

    }



    return value;

}



// ===============================
// ECG GRID
// ===============================

function drawECGGrid(){



    const width =
    canvas.width;


    const height =
    canvas.height;



    ctx.save();



    ctx.strokeStyle =
    "rgba(0,255,136,0.08)";


    ctx.lineWidth = 1;



    const smallGrid = 25;



    for(

        let x = 0;

        x <= width;

        x += smallGrid

    ){

        ctx.beginPath();


        ctx.moveTo(
            x,
            0
        );


        ctx.lineTo(
            x,
            height
        );


        ctx.stroke();

    }



    for(

        let y = 0;

        y <= height;

        y += smallGrid

    ){

        ctx.beginPath();


        ctx.moveTo(
            0,
            y
        );


        ctx.lineTo(
            width,
            y
        );


        ctx.stroke();

    }



    ctx.strokeStyle =
    "rgba(0,255,136,0.14)";


    const largeGrid = 125;



    for(

        let x = 0;

        x <= width;

        x += largeGrid

    ){

        ctx.beginPath();


        ctx.moveTo(
            x,
            0
        );


        ctx.lineTo(
            x,
            height
        );


        ctx.stroke();

    }



    for(

        let y = 0;

        y <= height;

        y += largeGrid

    ){

        ctx.beginPath();


        ctx.moveTo(
            0,
            y
        );


        ctx.lineTo(
            width,
            y
        );


        ctx.stroke();

    }



    ctx.restore();

}



// ===============================
// BASELINE
// ===============================

function drawBaseline(){



    ctx.save();



    ctx.strokeStyle =
    "rgba(0,255,136,0.15)";


    ctx.lineWidth = 1;



    ctx.beginPath();


    ctx.moveTo(
        0,
        canvas.height * 0.58
    );


    ctx.lineTo(
        canvas.width,
        canvas.height * 0.58
    );


    ctx.stroke();



    ctx.restore();

}



// ===============================
// ECG LABELS
// ===============================

function drawECGLabels(){



    ctx.save();



    ctx.font =
    "bold 14px Arial";


    ctx.textAlign =
    "center";


    ctx.fillStyle =
    "rgba(255,255,255,0.8)";



    const pX =
    mapECGTimeToScreen(120);


    const qrsX =
    mapECGTimeToScreen(340);


    const tX =
    mapECGTimeToScreen(590);



    if(

        pX >= 0 &&

        pX <= canvas.width

    ){

        ctx.fillText(
            "P",
            pX,
            35
        );

    }



    if(

        qrsX >= 0 &&

        qrsX <= canvas.width

    ){

        ctx.fillText(
            "QRS",
            qrsX,
            35
        );

    }



    if(

        tX >= 0 &&

        tX <= canvas.width

    ){

        ctx.fillText(
            "T",
            tX,
            35
        );

    }



    ctx.restore();

}



// ===============================
// MAP ECG TIME
// ===============================

function mapECGTimeToScreen(
    waveformTime
){



    const currentTime =

    heartState.ecgTime %

    baseCycleLength;



    let delta =

    waveformTime -

    currentTime;



    if(delta < 0){

        delta +=

        baseCycleLength;

    }



    const ratio =

    delta /

    sweepDuration;



    return (

        heartState.sweepPosition

        +

        ratio *
        canvas.width

    );

}



// ===============================
// ECG SWEEP
// ===============================

function drawECGSweep(){



    ctx.clearRect(

        0,

        0,

        canvas.width,

        canvas.height

    );



    drawECGGrid();


    drawBaseline();



    if(

        ecgPoints.length >= 2

    ){

        ctx.save();



        ctx.beginPath();



        for(

            let i = 0;

            i < ecgPoints.length;

            i++

        ){

            const point =
            ecgPoints[i];



            if(i === 0){

                ctx.moveTo(

                    point.x,

                    point.y

                );

            }

            else{

                ctx.lineTo(

                    point.x,

                    point.y

                );

            }

        }



        ctx.strokeStyle =
        "#00ff88";


        ctx.lineWidth = 3;


        ctx.lineJoin =
        "round";


        ctx.lineCap =
        "round";


        ctx.stroke();



        ctx.restore();

    }



    drawSweepCursor();


    drawECGLabels();

}



// ===============================
// SWEEP CURSOR
// ===============================

function drawSweepCursor(){



    const x =
    heartState.sweepPosition;



    ctx.save();



    ctx.strokeStyle =
    "rgba(255,255,255,0.55)";


    ctx.lineWidth = 1;



    ctx.beginPath();


    ctx.moveTo(
        x,
        0
    );


    ctx.lineTo(
        x,
        canvas.height
    );


    ctx.stroke();



    ctx.restore();

}



// ===============================
// ADD ECG POINT
// ===============================

function addECGPoint(){



    const x =
    heartState.sweepPosition;



    const value =
    ecgValue(
        heartState.ecgTime
    );



    const y =

    canvas.height * 0.58

    -

    value;



    ecgPoints.push({

        x:x,

        y:y

    });

}



// ===============================
// RESET ECG
// ===============================

function resetECGSweep(){



    ecgPoints = [];


    heartState.sweepPosition =
    0;


    addECGPoint();

}



// ===============================
// UPDATE ECG SWEEP
// ===============================

function updateECGSweep(
    deltaTime
){



    const sweepProgress =

    (

        deltaTime *

        animationSpeed *

        BASE_SPEED_FACTOR

    )

    /

    sweepDuration;



    heartState.sweepPosition +=

    sweepProgress *

    canvas.width;



    if(

        heartState.sweepPosition >=

        canvas.width

    ){

        heartState.sweepPosition =

        0;


        ecgPoints = [];


        addECGPoint();

    }

    else{

        addECGPoint();

    }



    drawECGSweep();

}



// ===============================
// SIMULATION UPDATE
// ===============================

function updateSimulation(
    deltaTime
){



    const actualDelta =

    deltaTime *

    animationSpeed *

    BASE_SPEED_FACTOR;



    heartState.ecgTime +=

    actualDelta;



    updateConduction();


    updateTimeline();


    updateECGSweep(
        deltaTime
    );

}



// ===============================
// CONDUCTION UPDATE
// ===============================

function updateConduction(
    forceStateSync = false
){

    const currentTime =
    heartState.ecgTime %
    baseCycleLength;

    let newStep = -1;

    for(
        let i = 0;
        i < conductionSteps.length;
        i++
    ){
        const step =
        conductionSteps[i];

        if(
            currentTime >= step.start &&
            currentTime < step.end
        ){
            newStep = i;
            break;
        }
    }

    const stepChanged =
    newStep !== heartState.currentStep;

    if(stepChanged){
        heartState.currentStep =
        newStep;

        renderStep();
    }

    // All visible simulation feedback is derived from the same ecgTime.
    // Event changes must also update the Current Phase ECG label even when
    // the broader conduction step has not changed (e.g. ST → T).
    updateECGEventIndicator(
        currentTime,
        stepChanged || forceStateSync
    );

    updateElectricalPulse(
        currentTime
    );

    updateCardiacRegions(
        currentTime
    );

}



// ===============================
// ECG EVENT / PHASE INDICATOR
// ===============================

function getCurrentECGEvent(
    currentTime
){

    for(

        let i = 0;

        i < ecgEvents.length;

        i++

    ){

        const event =
        ecgEvents[i];



        if(

            currentTime >= event.start &&

            currentTime < event.end

        ){

            return event;

        }

    }



    return ecgEvents[0];

}



function updateECGEventIndicator(
    currentTime,
    forceRender = false
){

    const event =
    getCurrentECGEvent(
        currentTime
    );



    const eventChanged =
    heartState.currentECGEvent !== event.id;



    if(eventChanged || forceRender){

        heartState.currentECGEvent =
        event.id;

        ecgEventIndicator.textContent =
        event.label;

        // Current Phase shows the same ECG event derived from ecgTime.
        // This prevents stale values such as "ST / T Wave" from remaining
        // after the timeline enters the T-wave portion of the same phase.
        phaseECG.textContent =
        event.label;

        eventSyncStatus.textContent =
        heartState.playing
            ? "Synchronized with the current ECG cycle."
            : "Paused at the current ECG event.";

    }



    const explanationOutOfSync =
    selectedECGComponent !== event.id;

    if(!eventChanged && !forceRender && !explanationOutOfSync){

        return;

    }



    // During playback, the current ECG event has priority.
    // A click can still be used for manual inspection while paused.
    if(eventChanged || forceRender || (heartState.playing && explanationOutOfSync)){

        syncECGExplanationToEvent(event.id);

    }



    document
    .querySelectorAll(
        ".ecg-item"
    )
    .forEach(

        el =>

        el.classList.remove(
            "ecg-active"
        )

    );



    if(

        event.id !== "Baseline"

    ){

        highlightECG(
            event.id
        );

    }

}



function updateConductionFlowIndicator(){

    eventFlowItems.forEach(

        item => {

            item.classList.remove(
                "event-active"
            );

        }

    );



    const step =
    conductionSteps[
        heartState.currentStep
    ];



    if(!step){

        return;

    }



    let target =
    step.id;



    if(

        step.id === "Branches" ||
        step.id === "Purkinje"

    ){

        target = "Purkinje";

    }



    eventFlowItems.forEach(

        item => {

            if(

                item.dataset.conduction ===
                target

            ){

                item.classList.add(
                    "event-active"
                );

            }

        }

    );

}



// ===============================
// CLEAR HEART
// ===============================

function clearHeart(){



    document
    .querySelectorAll(
        ".active-node"
    )
    .forEach(

        el =>

        el.classList.remove(
            "active-node"
        )

    );



    document
    .querySelectorAll(
        ".active-path"
    )
    .forEach(

        el =>

        el.classList.remove(
            "active-path"
        )

    );



    atriaRegion
    .classList.remove(
        "atria-active"
    );



    ventricleRegion
    .classList.remove(
        "ventricles-active"
    );



    ventricleRegion
    .classList.remove(
        "ventricles-recovery"
    );

}



// ===============================
// RENDER STEP
// ===============================

function renderStep(){



    clearHeart();


    clearECGHighlights();



    const step =

    conductionSteps[
        heartState.currentStep
    ];



    if(!step){

        phaseTitle.textContent =
        "Ready";


        phaseDescription.textContent =
        "Press Play to begin the cardiac conduction cycle.";


        phaseECG.textContent =
        "Ready";

        updateConductionFlowIndicator();

        return;

    }



    phaseTitle.textContent =
    step.title;



    phaseDescription.textContent =
    step.description;



    const phaseEvent =
    getCurrentECGEvent(
        heartState.ecgTime % baseCycleLength
    );

    phaseECG.textContent =
    phaseEvent.label;


    updateConductionFlowIndicator();



    // =========================
    // SA
    // =========================

    if(

        step.id === "SA"

    ){

        document
        .getElementById("SA")
        .classList.add(
            "active-node"
        );


        atriaRegion
        .classList.add(
            "atria-active"
        );


        highlightECG("P");

    }



    // =========================
    // AV
    // =========================

    else if(

        step.id === "AV"

    ){

        document
        .getElementById("AV")
        .classList.add(
            "active-node"
        );


        document
        .getElementById("AVPath")
        .classList.add(
            "active-path"
        );


        highlightECG("PR");

    }



    // =========================
    // HIS
    // =========================

    else if(

        step.id === "His"

    ){

        document
        .getElementById("His")
        .classList.add(
            "active-node"
        );


        document
        .getElementById("HisPath")
        .classList.add(
            "active-path"
        );


        highlightECG("PR");

    }



    // =========================
    // BRANCHES
    // =========================

    else if(

        step.id === "Branches"

    ){

        document
        .getElementById("RBB")
        .classList.add(
            "active-path"
        );


        document
        .getElementById("LBB")
        .classList.add(
            "active-path"
        );


        highlightECG("QRS");

    }



    // =========================
    // PURKINJE
    // =========================

    else if(

        step.id === "Purkinje"

    ){

        document
        .getElementById("Purkinje")
        .classList.add(
            "active-node"
        );


        document
        .getElementById("RBB")
        .classList.add(
            "active-path"
        );


        document
        .getElementById("LBB")
        .classList.add(
            "active-path"
        );


        ventricleRegion
        .classList.add(
            "ventricles-active"
        );


        highlightECG("QRS");

    }



    // =========================
    // RECOVERY
    // =========================

    else if(

        step.id === "Recovery"

    ){

        ventricleRegion
        .classList.add(
            "ventricles-recovery"
        );


        highlightECG("ST");


        highlightECG("T");

    }

}



// ===============================
// ECG HIGHLIGHTS
// ===============================

function clearECGHighlights(){



    document
    .querySelectorAll(
        ".ecg-item"
    )
    .forEach(

        el =>

        el.classList.remove(
            "ecg-active"
        )

    );

}



// ===============================
// HIGHLIGHT ECG
// ===============================

function highlightECG(
    type
){



    document
    .querySelectorAll(
        ".ecg-item"
    )
    .forEach(

        item => {

            const label =

            item
            .querySelector(
                ".ecg-label"
            );



            if(

                label &&

                label.textContent.trim()
                === type

            ){

                item.classList.add(
                    "ecg-active"
                );

            }

        }

    );

}



// ===============================
// CARDIAC REGIONS
// ===============================

function updateCardiacRegions(
    time
){



    // ATRIAL DEPOLARIZATION

    if(

        time >= 80 &&

        time <= 160

    ){

        atriaRegion
        .classList.add(
            "atria-active"
        );

    }

    else{

        atriaRegion
        .classList.remove(
            "atria-active"
        );

    }



    // VENTRICULAR DEPOLARIZATION

    if(

        time >= 300 &&

        time <= 450

    ){

        ventricleRegion
        .classList.remove(
            "ventricles-recovery"
        );


        ventricleRegion
        .classList.add(
            "ventricles-active"
        );

    }



    // VENTRICULAR RECOVERY

    else if(

        time >= 500 &&

        time <= 680

    ){

        ventricleRegion
        .classList.remove(
            "ventricles-active"
        );


        ventricleRegion
        .classList.add(
            "ventricles-recovery"
        );

    }



    else{

        ventricleRegion
        .classList.remove(
            "ventricles-active"
        );


        ventricleRegion
        .classList.remove(
            "ventricles-recovery"
        );

    }

}



// ===============================
// ELECTRICAL PULSE
// ===============================

function updateElectricalPulse(
    time
){

    /*
     * v1.7 patch4:
     * Make the ventricular conduction split explicit.
     * The existing simulation clock remains the sole time source.
     */

    let x = 250;
    let y = 160;

    // Default: one main pulse, branch pulses hidden.
    conductionPulse.style.opacity = "1";
    conductionPulseR.style.opacity = "0";
    conductionPulseL.style.opacity = "0";

    // SA Node
    if(
        time < 130
    ){

        x = 250;
        y = 160;

    }

    // SA → AV
    else if(
        time >= 130 &&
        time < 250
    ){

        const progress =
        (
            time - 130
        ) / 120;

        x = 250;

        y =
        160 +
        progress * 60;

    }

    // AV → His
    else if(
        time >= 250 &&
        time < 305
    ){

        const progress =
        (
            time - 250
        ) / 55;

        x = 250;

        y =
        220 +
        progress * 60;

    }

    // His → Bundle Branch bifurcation
    else if(
        time >= 305 &&
        time < 380
    ){

        const progress =
        (
            time - 305
        ) / 75;

        x = 250;

        y =
        280 +
        progress * 80;

    }

    // Explicit RBB + LBB propagation
    else if(
        time >= 380 &&
        time < 450
    ){

        const progress =
        (
            time - 380
        ) / 70;

        conductionPulse.style.opacity = "0";

        conductionPulseR.style.opacity = "1";
        conductionPulseL.style.opacity = "1";

        const rightX =
        250 +
        progress * 90;

        const rightY =
        280 +
        progress * 80;

        const leftX =
        250 -
        progress * 90;

        const leftY =
        280 +
        progress * 80;

        conductionPulseR.setAttribute(
            "cx",
            rightX
        );

        conductionPulseR.setAttribute(
            "cy",
            rightY
        );

        conductionPulseL.setAttribute(
            "cx",
            leftX
        );

        conductionPulseL.setAttribute(
            "cy",
            leftY
        );

        return;

    }

    // No active conduction pulse during recovery/rest.
    else{

        conductionPulse.style.opacity = "0";

    }

    conductionPulse.setAttribute(
        "cx",
        x
    );

    conductionPulse.setAttribute(
        "cy",
        y
    );

}



// ===============================
// TIMELINE
// ===============================

function updateTimeline(){



    const currentTime =

    heartState.ecgTime %

    baseCycleLength;



    slider.value =

    (

        currentTime /

        baseCycleLength

    ) * 100;

}



// ===============================
// ANIMATION LOOP
// ===============================

function animationLoop(
    timestamp
){



    if(

        !heartState.playing

    ){

        return;

    }



    if(

        heartState.lastTimestamp === null

    ){

        heartState.lastTimestamp =
        timestamp;

    }



    const deltaTime =

    Math.min(

        timestamp -

        heartState.lastTimestamp,

        50

    );



    heartState.lastTimestamp =
    timestamp;



    updateSimulation(
        deltaTime
    );



    requestAnimationFrame(
        animationLoop
    );

}



// ===============================
// PLAY
// ===============================

function play(){



    if(

        heartState.playing

    ){

        return;

    }



    heartState.playing =
    true;



    heartState.lastTimestamp =
    null;



    requestAnimationFrame(
        animationLoop
    );

}



// ===============================
// PAUSE
// ===============================

function pause(){



    heartState.playing =
    false;



    heartState.lastTimestamp =
    null;



    drawECGSweep();

}



// ===============================
// RESET
// ===============================

function reset(){



    pause();



    heartState.ecgTime =
    0;



    heartState.currentStep =
    -1;



    heartState.currentECGEvent =
    null;



    heartState.sweepPosition =
    0;



    slider.value =
    0;



    resetECGSweep();



    conductionPulse
    .setAttribute(
        "cx",
        250
    );


    conductionPulse
    .setAttribute(
        "cy",
        160
    );

    conductionPulse.style.opacity = "1";

    conductionPulseR.style.opacity = "0";
    conductionPulseL.style.opacity = "0";

    conductionPulseR.setAttribute(
        "cx",
        250
    );

    conductionPulseR.setAttribute(
        "cy",
        280
    );

    conductionPulseL.setAttribute(
        "cx",
        250
    );

    conductionPulseL.setAttribute(
        "cy",
        280
    );



    clearHeart();

    clearECGHighlights();

    // Reset starts from the beginning of the cycle and clears any manual
    // component selection before rebuilding the canonical feedback state.
    selectedECGComponent = null;

    ecgComponentItems.forEach(
        item => item.classList.remove(
            "ecg-selected"
        )
    );

    renderStep();

    // Reset returns the interface to the pre-playback Ready state.
    // The timeline remains at 0, but no active simulation phase is shown
    // until playback or an explicit timeline seek starts the state machine.
    heartState.currentECGEvent = null;
    ecgEventIndicator.textContent = "Ready";
    eventSyncStatus.textContent =
    "Press Play to begin synchronization.";
    phaseECG.textContent = "Ready";

    ecgExplanationTitle.textContent =
    "Select an ECG component";
    ecgExplanationText.textContent =
    "Click P, PR, QRS, ST, or T above to see how the ECG component relates to cardiac electrical activity.";
    ecgExplanationLink.textContent = "—";

    drawECGSweep();

}



// ===============================
// TIMELINE SLIDER
// ===============================

slider.oninput =
function(){



    pause();



    const percent =

    Number(
        slider.value
    ) / 100;



    heartState.ecgTime =

    baseCycleLength *

    percent;



    heartState.sweepPosition =

    percent *

    canvas.width;



    ecgPoints = [];



    const pointCount =

    Math.max(

        1,

        Math.floor(
            heartState.sweepPosition
        )

    );



    for(

        let i = 0;

        i <= pointCount;

        i++

    ){

        const ratio =

        i /

        canvas.width;



        const sampleTime =

        heartState.ecgTime

        -

        (

            1 - ratio

        )

        *

        sweepDuration

        *

        BASE_SPEED_FACTOR;



        ecgPoints.push({

            x:i,

            y:

            canvas.height / 2

            -

            ecgValue(
                sampleTime
            )

        });

    }



    updateConduction(true);


    drawECGSweep();

};



// ===============================
// HEART RATE SLIDER
// ===============================

heartRateSlider.oninput =
function(){



    heartRate =

    Number(
        heartRateSlider.value
    );



    updateHeartRateUI();

};



// ===============================
// BUTTON EVENTS
// ===============================

playBtn.onclick =
play;


pauseBtn.onclick =
pause;


resetBtn.onclick =
reset;



// ===============================
// INITIALIZATION
// ===============================

heartRateSlider.value =
80;


heartRate =
80;


animationSpeed =
1.0;


updateHeartRateUI();


resetECGSweep();


renderStep();

updateECGEventIndicator(0);


drawECGSweep();