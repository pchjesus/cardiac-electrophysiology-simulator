/*
 * Cardiac Electrophysiology Simulator v1.10 Patch 1
 * Wiggers model foundation (NO drawing loop, DOM mutation, or independent clock).
 *
 * All pressures are v1.9 relative teaching indexes; they are intentionally
 * DISCONTINUOUS at several stage boundaries. Never plot as calibrated mmHg or
 * silently interpolate them. Ventricular volume is a relative teaching scale,
 * not milliliters or ejection fraction.
 */
(function (root) {
    'use strict';

    function createWiggersModel(getMechanicalTiming, getMechanicalState) {
        if (typeof getMechanicalTiming !== 'function' ||
            typeof getMechanicalState !== 'function') {
            throw new TypeError('Wiggers requires the v1.9 mechanical model functions');
        }

        const MODEL_INFO = Object.freeze({
            version: '1.10-patch1',
            scope: 'normal-sinus-cycle',
            pressureUnit: 'relative-teaching-index',
            pressureProfile: 'v1.9-discontinuous-stage-values',
            ventricularVolumeUnit: 'normalized-relative',
            referenceSide: 'left-heart conceptual proxy',
            calibratedForPatients: false,
            heartSounds: 'left-sided S1/S2 event markers only',
            limitation: 'No clinical pressure, volume, cardiac output, EF, or sound splitting'
        });

        function validateTiming(electrical) {
            if (!electrical || !Number.isFinite(electrical.rr) || electrical.rr <= 0 ||
                !['pStart', 'pEnd', 'qrsStart', 'qrsEnd', 'stEnd', 'tEnd'].every(
                    key => Number.isFinite(electrical[key])
                )) {
                throw new TypeError('A finite, positive-RR physiological electrical timing is required');
            }
        }

        function normalizePhase(phaseMs, rrMs) {
            if (!Number.isFinite(phaseMs)) {
                throw new TypeError('Wiggers phase must be a finite number of physiological milliseconds');
            }
            return ((phaseMs % rrMs) + rrMs) % rrMs;
        }

        function getValveEvents(electrical) {
            validateTiming(electrical);
            const t = getMechanicalTiming(electrical);
            // One representative left-sided event per valve group. Do not
            // imply independently computed RV/LV timings or S1/S2 splitting.
            return [
                { id: 'mitral-close', type: 'valve-close', valve: 'mitral', timeMs: t.contractionStart },
                { id: 'aortic-open', type: 'valve-open', valve: 'aortic', timeMs: t.ejectionStart },
                { id: 'aortic-close', type: 'valve-close', valve: 'aortic', timeMs: t.ejectionEnd },
                { id: 'mitral-open', type: 'valve-open', valve: 'mitral', timeMs: t.relaxationEnd }
            ];
        }

        function getHeartSoundEvents(electrical) {
            validateTiming(electrical);
            const t = getMechanicalTiming(electrical);
            return [
                { id: 'S1', type: 'heart-sound-marker', timeMs: t.contractionStart,
                  linkedValveEvent: 'mitral-close' },
                { id: 'S2', type: 'heart-sound-marker', timeMs: t.ejectionEnd,
                  linkedValveEvent: 'aortic-close' }
            ];
        }

        function getSnapshot(phaseMs, electrical) {
            validateTiming(electrical);
            const phase = normalizePhase(phaseMs, electrical.rr);
            const state = getMechanicalState(phase, electrical);
            return {
                metadata: MODEL_INFO,
                cycle: { rrMs: electrical.rr, phaseMs: phase, heartRateBpm: 60000 / electrical.rr },
                electrical: {
                    pStartMs: electrical.pStart, pEndMs: electrical.pEnd,
                    qrsStartMs: electrical.qrsStart, qrsEndMs: electrical.qrsEnd,
                    stEndMs: electrical.stEnd, tEndMs: electrical.tEnd
                },
                mechanical: { stage: state.stage, progress: state.progress,
                              boundaries: { ...state.boundaries } },
                pressure: {
                    leftAtrial: state.pressure.atrial,
                    leftVentricular: state.pressure.ventricular,
                    aortic: state.pressure.arterial,
                    representation: 'discontinuous-relative-index'
                },
                ventricularVolume: { relativeValue: state.ventricularVolume },
                valves: { mitral: state.valves.mitral, aortic: state.valves.aortic },
                flow: state.flow,
                valveEvents: getValveEvents(electrical),
                heartSoundEvents: getHeartSoundEvents(electrical)
            };
        }

        function inspectPressureBoundaries(electrical, epsilonMs = 0.0001) {
            validateTiming(electrical);
            if (!Number.isFinite(epsilonMs) || epsilonMs <= 0 || epsilonMs >= 1) {
                throw new RangeError('Pressure-boundary epsilon must be finite, positive and <1 ms');
            }
            const t = getMechanicalTiming(electrical);
            const boundaries = [
                ['cycle-start', 0],
                ['atrial-start', t.atrialStart],
                ['contraction-start', t.contractionStart],
                ['ejection-start', t.ejectionStart],
                ['ejection-end', t.ejectionEnd],
                ['relaxation-end', t.relaxationEnd]
            ];
            return boundaries.map(([id, timeMs]) => {
                const before = getMechanicalState(
                    normalizePhase(timeMs - epsilonMs, t.rr), electrical).pressure;
                const after = getMechanicalState(
                    normalizePhase(timeMs, t.rr), electrical).pressure;
                const jumps = {
                    leftAtrial: after.atrial - before.atrial,
                    leftVentricular: after.ventricular - before.ventricular,
                    aortic: after.arterial - before.arterial
                };
                return {
                    id, timeMs, deltaRelativeIndex: jumps,
                    discontinuous: Object.values(jumps).some(delta => Math.abs(delta) > 0.001)
                };
            });
        }

        return Object.freeze({
            metadata: MODEL_INFO,
            getSnapshot,
            getValveEvents,
            getHeartSoundEvents,
            inspectPressureBoundaries
        });
    }

    if (typeof module !== 'undefined' && module.exports) {
        module.exports = { createWiggersModel };
    }
    if (root && root.CardiacMechanical) {
        root.CardiacWiggers = createWiggersModel(
            root.CardiacMechanical.getMechanicalTiming,
            root.CardiacMechanical.getMechanicalState
        );
    }
})(typeof window !== 'undefined' ? window : null);
