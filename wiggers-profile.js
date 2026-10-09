/*
 * v1.10 Patch 2 — continuous educational *relative* left-heart pressure /
 * volume profile. Parallel to, not a replacement for, mechanics.js v1.9.
 *
 * All values are heuristic dimensionless indexes, NOT mmHg, mL, EF, patient
 * measurements, or a quantitatively calibrated pressure-volume simulation.
 * Boundaries are inherited from the existing electromechanical model.
 * The valve event schedule is authoritative exactly at pressure equality.
 * No DOM access, rAF, timer, mutable state or side effects.
 */
(function (root) {
    'use strict';

    function createWiggersProfile(getMechanicalTiming, wiggers) {
        if (typeof getMechanicalTiming !== 'function' || !wiggers ||
            typeof wiggers.getValveEvents !== 'function' ||
            typeof wiggers.getHeartSoundEvents !== 'function') {
            throw new TypeError('Continuous profile requires mechanical timing and v1.10 Patch 1 events');
        }

        const metadata = Object.freeze({
            version: '1.10-patch2',
            scope: 'normal-sinus-left-heart-teaching-proxy',
            pressureUnit: 'relative-teaching-index',
            pressureProfile: 'continuous-heuristic-C1',
            volumeUnit: 'normalized-relative',
            pressureCalibrated: false,
            separateRightHeartModel: false,
            boundaryConvention: 'half-open-stages; valve-events-own-equality',
            limitations: 'No mmHg, mL, EF, contractility, arterial compliance or S1/S2 splitting'
        });
        const smooth = u => u * u * (3 - 2 * u);
        const mix = (a, b, u) => a + (b - a) * smooth(u);

        function requireElectrical(e) {
            if (!e || !Number.isFinite(e.rr) || e.rr <= 0 ||
                !['pStart', 'pEnd', 'qrsStart', 'qrsEnd', 'stEnd', 'tEnd'].every(
                    name => Number.isFinite(e[name])
                )) throw new TypeError('Valid finite ECG timing required');
        }

        function boundaries(e) {
            requireElectrical(e);
            const t = getMechanicalTiming(e);
            if (!t || ![t.atrialStart,t.contractionStart,t.ejectionStart,
                t.ejectionEnd,t.relaxationEnd,t.rr].every(Number.isFinite) ||
                !(0 < t.atrialStart && t.atrialStart < t.contractionStart &&
                  t.contractionStart < t.ejectionStart &&
                  t.ejectionStart < t.ejectionEnd &&
                  t.ejectionEnd < t.relaxationEnd && t.relaxationEnd < t.rr)) {
                throw new RangeError('Mechanical phase boundaries must be finite and ordered');
            }
            return t;
        }

        function getLandmarks(e) {
            const t = boundaries(e);
            // These values are intentionally chosen for qualitative teaching.
            // Adjacent segments share the same endpoint; the final equals t=0.
            return [
                { id:'cycle-start',      timeMs:0,                    a:12,v:8, aorta:81, volume:0.88 },
                { id:'atrial-start',     timeMs:t.atrialStart,        a:14,v:9, aorta:79, volume:0.88 },
                { id:'mitral-close',     timeMs:t.contractionStart,   a:15,v:15,aorta:77, volume:1.00 },
                { id:'aortic-open',      timeMs:t.ejectionStart,      a:11,v:77,aorta:77, volume:1.00 },
                { id:'aortic-close',     timeMs:t.ejectionEnd,        a:10,v:90,aorta:90, volume:0.48 },
                { id:'mitral-open',      timeMs:t.relaxationEnd,      a:12,v:12,aorta:87, volume:0.48 },
                { id:'cycle-end',        timeMs:t.rr,                 a:12,v:8, aorta:81, volume:0.88 }
            ];
        }

        // For nonnegative times the single modulo avoids v1.9 double-modulo
        // rounding at exact positive event timestamps. Negative phases wrap.
        // Inputs outside a cycle can still have normal IEEE-754 rounding.
        function phaseWithinCycle(phaseMs, rr) {
            if (!Number.isFinite(phaseMs)) throw new TypeError('A finite physiological phase is required');
            const rem = phaseMs % rr;
            return rem < 0 ? rem + rr : rem;
        }

        function getSnapshot(phaseMs, electrical) {
            const t = boundaries(electrical);
            const p = phaseWithinCycle(phaseMs,t.rr);
            const anchors = getLandmarks(electrical);
            let index = anchors.length - 2;
            for (let i=0;i<anchors.length-1;i++) {
                if (p < anchors[i+1].timeMs) { index=i; break; }
            }
            const from=anchors[index], to=anchors[index+1];
            const u=(p-from.timeMs)/(to.timeMs-from.timeMs);
            const progress=smooth(u);
            const pressure={
                leftAtrial:mix(from.a,to.a,u),
                leftVentricular:mix(from.v,to.v,u),
                aortic:mix(from.aorta,to.aorta,u),
                representation:'continuous-heuristic-relative-index'
            };
            // A rounded, C1-smooth ejection arch is greater in the LV than
            // the aorta only between open/close events; gradients are zero
            // at those two event instants, and the event schedule breaks ties.
            if (index===3) {
                const arch=Math.sin(Math.PI*u)**2;
                pressure.aortic+=20*arch;
                pressure.leftVentricular=pressure.aortic+12*arch;
            }
            const stage=['filling','atrial_systole','isovolumetric_contraction',
                         'ejection','isovolumetric_relaxation','filling'][index];
            const valves={
                mitral:p<t.contractionStart || p>=t.relaxationEnd,
                aortic:p>=t.ejectionStart && p<t.ejectionEnd
            };
            const gradients={
                mitral:pressure.leftAtrial-pressure.leftVentricular,
                aortic:pressure.leftVentricular-pressure.aortic
            };
            return {
                metadata,
                cycle:{rrMs:t.rr,phaseMs:p,heartRateBpm:60000/t.rr},
                mechanical:{stage,progress,boundaries:{...t}},
                pressure,
                ventricularVolume:{relativeValue:mix(from.volume,to.volume,u)},
                valves,
                pressureGradients:gradients,
                flow:valves.aortic?'ejection':valves.mitral?'filling':'none',
                valveEvents:wiggers.getValveEvents(electrical),
                heartSoundEvents:wiggers.getHeartSoundEvents(electrical)
            };
        }

        return Object.freeze({metadata,getSnapshot,getLandmarks,phaseWithinCycle});
    }

    if (typeof module !== 'undefined' && module.exports) {
        module.exports={createWiggersProfile};
    }
    if (root && root.CardiacMechanical && root.CardiacWiggers) {
        root.CardiacWiggersProfile=createWiggersProfile(
            root.CardiacMechanical.getMechanicalTiming,root.CardiacWiggers
        );
    }
})(typeof window !== 'undefined' ? window : null);
