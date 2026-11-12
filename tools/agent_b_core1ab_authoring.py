"""Agent B authoring corrections: synthetic practice only, never original Core2 edits.

Existing builder scripts invoke these functions on their authored Core1B objects.
Human Physics/QRT review remains mandatory even when checks pass.
"""
from __future__ import annotations

import copy
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path


def inverse_lens_core1b(original: dict) -> dict:
    b = copy.deepcopy(original)
    b["fresh_context_ref"] = "AB-PRACTICE-PHYS-OPT-INVERSE-DISPLACEMENT-R1"
    b["protected_fresh_inference_W"] = (
        "Infer focal length from independently observed conjugate-position separation "
        "rather than compute the original exam's lens positions from given focal length."
    )
    b["taught_skill_Y"] = "Apply paraxial thin-lens geometry and real-image existence D >= 4f."
    b["connecting_route_Z"] = "Treat measured position separation as the difference of quadratic roots."
    b["stages"] = {
        "stage_1_predict": {
            "prompt": "Two sharp-image lens positions have been measured. Can their separation determine an unknown focal length? Explain before calculating.",
            "defensible_prediction": "Yes, provided the screen separation and real-image thin-lens assumptions are known."
        },
        "stage_2_attempt": {
            "prompt": "An object and screen are 96 cm apart. The two lens positions yielding a sharp image differ by 48 cm. Infer the convex lens focal length, both lens positions and their magnification magnitudes. Justify the physical assumptions.",
            "produces": "f = 18 cm; x = 24 and 72 cm; |m| = 3 and 1/3.",
            "closure": "RUBRIC",
            "rubric": [
                {"criterion": "Use sum of positive lens-position roots D=96 and separation d=48.", "evidence_of": "Distinguishes measured root separation from focal length."},
                {"criterion": "Infer f=(D^2-d^2)/(4D), with D >= 4f.", "evidence_of": "Derives inverse relation rather than presuming source focal length."},
                {"criterion": "Obtain x1=24 cm and x2=72 cm, then |m|=3 and 1/3.", "evidence_of": "Checks conjugacy and both physical magnification magnitudes."}
            ],
            "accepted": ["f = 18 cm with x1=24, x2=72 cm and magnification magnitudes 3 and 1/3"],
            "rejected": ["f = 48 cm because displacement is focal length", "One position only", "Claim that image always forms for any D"]
        },
        "stage_3_reconstruct": {
            "route": [
                {"ask": "Which two measured quantities correspond to the sum and difference of the lens-position roots?", "why_this_ask": "The two roots sum to D; their positive separation is measured independently.", "step_answer": "x1+x2=96 cm, x2-x1=48 cm."},
                {"ask": "How does their product determine the focal length?", "why_this_ask": "The thin-lens quadratic has product Df.", "step_answer": "x1*x2=(D^2-d^2)/4=Df, so f=(96^2-48^2)/(4*96)=18 cm."},
                {"ask": "Where are the physical conjugate lens positions?", "why_this_ask": "Recover roots from measured sum and difference.", "step_answer": "x1=(96-48)/2=24 cm; x2=(96+48)/2=72 cm."},
                {"ask": "What are the two magnification magnitudes?", "why_this_ask": "Use |m|=(D-x)/x with real images.", "step_answer": "At 24 cm, |m|=72/24=3. At 72 cm, |m|=24/72=1/3."}
            ],
            "differs_from_teaching_path": "Inverse measurement-to-focal-length reasoning; no original 75 cm / 12 cm values."
        },
        "stage_4_diagnose": {
            "error_trap": "Confusing the measured difference of lens positions with focal length.",
            "diagnostic_prompt": "If you used f=d, what measured constraint did your model neglect?",
            "resolution": "The two positions are roots of x(D-x)=Df; their separation alone is not f."
        },
        "stage_5_repair": {"action": "Write both sum and difference constraints, infer product, then reconstruct f and both magnifications. Retain the original attempt separately."},
        "stage_6_boundary_test": {
            "prompt": "The screen distance becomes 70 cm with the same lens. Without trial positions, determine if any sharp real image can form.",
            "answer": "No: 70 cm < 4f=72 cm, so the real-position quadratic has negative discriminant."
        }
    }
    b["progressive_hints"] = [
        {"hint_id": "H1", "tier": "CLARIFY", "text": "The measured separation is between two physically valid lens positions, not the focal length."},
        {"hint_id": "H2", "tier": "CORRELATE", "text": "The sum and difference of the two position roots are known; use them to determine their product."},
        {"hint_id": "H3", "tier": "OPEN_THE_WAY", "text": "The product of the lens-position roots is Df. Use the observed sum and difference without presuming a particular value of f."}
    ]
    return b


def unequal_droplets_core1b(original: dict) -> dict:
    b = copy.deepcopy(original)
    b["fresh_context_ref"] = "AB-PRACTICE-PHYS-FLUID-UNEQUAL-DROPLETS-R1"
    b["protected_fresh_inference_W"] = (
        "Transfer equal-radius volume/area scaling to a mixed-radius collection, "
        "summing cubes and squares separately before computing the free-energy contribution."
    )
    b["taught_skill_Y"] = "Incompressible liquid volume conservation and spherical interface area formulas."
    b["connecting_route_Z"] = "For unequal drops use sum of cubic radii for final volume; separately sum squared radii for initial area."
    b["stages"] = {
        "stage_1_predict": {
            "prompt": "Would nine unequal droplets produce the same final radius as nine identical small droplets? Explain.",
            "defensible_answer": "No. Each droplet contributes a volume proportional to the cube of its individual radius."
        },
        "stage_2_attempt": {
            "prompt": "Eight water drops of radius 1 mm and one water drop of radius 2 mm merge into one spherical drop at constant liquid volume. With surface tension 0.072 N/m, calculate the final radius, total eliminated surface area and released surface-energy contribution. State assumptions.",
            "produces": "R=16^(1/3) mm; eliminated area approx 7.1005e-5 m^2; released surface-energy contribution approx 5.1124e-6 J.",
            "closure": "RUBRIC",
            "rubric": [
                {"criterion": "Sum 8*r^3 + (2r)^3 = 16*r^3 for liquid volume.", "evidence_of": "Does not treat the nine unequal drops as nine identical drops."},
                {"criterion": "Use initial area 4*pi*r^2*(8+4), final area 4*pi*r^2*16^(2/3).", "evidence_of": "Distinguishes cube scaling for volume from square scaling for area."},
                {"criterion": "Multiply positive area reduction by 0.072 N/m with correct units.", "evidence_of": "Reports a conditional surface-energy contribution, not guaranteed total process energy."}
            ],
            "accepted": ["R=16^(1/3) mm, area loss approx 7.1005e-5 m^2, energy approx 5.1124e-6 J"],
            "rejected": ["R=9^(1/3) mm", "Ignore the large drop's initial area", "Say energy release proves immediate merger under any conditions"]
        },
        "stage_3_reconstruct": {
            "route": [
                {"ask": "How is total liquid volume represented for unequal initial radii?", "why_this_ask": "Each spherical volume scales cubically.", "step_answer": "R^3=8*(1 mm)^3+(2 mm)^3=16 mm^3; R=16^(1/3) mm."},
                {"ask": "What is the initial area of all nine surfaces?", "why_this_ask": "Sum individual areas before merger.", "step_answer": "A_initial=4*pi*(8*(1 mm)^2+(2 mm)^2)=4*pi*12 mm^2."},
                {"ask": "What area remains afterward?", "why_this_ask": "The final sphere has the conserved volume.", "step_answer": "A_final=4*pi*16^(2/3) mm^2, so area reduction is about 7.1005e-5 m^2."},
                {"ask": "What is the surface-energy contribution and its validity limit?", "why_this_ask": "Use gamma*delta_area for constant gamma, not an unconditional kinetic claim.", "step_answer": "0.072 N/m times area reduction = 5.1124e-6 J, assuming spherical interfaces, incompressible liquid and constant gamma."}
            ],
            "differs_from_teaching_path": "Mixed initial radii require an independent volume and area sum, not N identical droplets."
        },
        "stage_4_diagnose": {
            "error_trap": "Treating the large drop as equal to the small drops or assuming release implies immediate merger.",
            "diagnostic_prompt": "Why would R=9^(1/3) mm violate the original material quantity?",
            "causal_explanation": "A 2-mm droplet contains eight times the 1-mm drop's volume; the total is 16, not 9, cubic-mm radius units."
        },
        "stage_5_repair": {"action": "Preserve your first response, write the nine individual volume and area contributions, then recompute."},
        "stage_6_boundary_test": {
            "prompt": "Replace the 2-mm drop with a third 1-mm drop, leaving ten identical 1-mm drops total. Which volume sum and area sum now apply?",
            "answer": "For ten equal 1-mm drops, R^3=10 mm^3 and A_initial=4*pi*10 mm^2; compare to the unequal-radius case."
        }
    }
    b["progressive_hints"] = [
        {"tier": 1, "text": "For the starting drops, sum volumes using each radius cubed."},
        {"tier": 2, "text": "Initial area is the sum of all nine spherical areas, not nine times the small-drop area."},
        {"tier": 3, "text": "A 2-mm drop has a different contribution to volume and area. Keep the two sums separate before applying gamma."}
    ]
    return b


class _Core1BPanelFinder(HTMLParser):
    def __init__(self, source: str):
        super().__init__(convert_charrefs=True)
        self.source = source
        self.lines = [0]
        for i, char in enumerate(source):
            if char == "\n":
                self.lines.append(i + 1)
        self.start = None
        self.end = None
        self.depth = 0

    def _offset(self):
        line, col = self.getpos()
        return self.lines[line - 1] + col

    def handle_starttag(self, tag, attrs):
        if tag != "div" or self.end is not None:
            return
        if self.start is None and dict(attrs).get("id") == "content-core1b":
            self.start = self._offset()
            self.depth = 1
        elif self.start is not None:
            self.depth += 1

    def handle_endtag(self, tag):
        if tag != "div" or self.start is None or self.end is not None:
            return
        self.depth -= 1
        if self.depth == 0:
            self.end = self._offset() + len("</div>")


ENGINE_JS = r"""
(function () {
  'use strict';
  function boot() {
    const root = document.querySelector('#content-core1b[data-agent-b-core1b]');
    if (!root) return;
    const data = JSON.parse(document.getElementById('agent-b-core1b-data').textContent);
    const key = ['g9v4','agent-b','core1b',root.dataset.sourceId,root.dataset.practiceId,root.dataset.revision].join(':');
    const by = role => root.querySelector('[data-role="' + role + '"]');
    const notify = (message, danger=false) => {
      by('status').textContent=message;
      by('status').setAttribute('role', danger ? 'alert' : 'status');
    };
    const nonblank = x => typeof x === 'string' && !!x.trim();
    const valid = x => !!x && x.schema==='agent-b-core1b-attempt/v1' &&
      x.key===key && x.revision===root.dataset.revision &&
      x.hints && typeof x.hints==='object' && !Array.isArray(x.hints) &&
      (!x.prediction || nonblank(x.prediction)) &&
      (!x.firstAttempt || (nonblank(x.firstAttempt.text) && nonblank(x.prediction))) &&
      (!x.diagnosis || (nonblank(x.diagnosis) && x.firstAttempt)) &&
      (!x.repair || (nonblank(x.repair) && x.diagnosis)) &&
      (!x.transfer || (nonblank(x.transfer) && x.repair));
    let priorRaw = null;
    let state = {schema:'agent-b-core1b-attempt/v1', key, revision:root.dataset.revision,
      prediction:null, firstAttempt:null, hints:{}, diagnosis:null, repair:null, transfer:null, events:[]};
    function lock(message) {
      root.querySelectorAll('textarea,button').forEach(e => e.disabled=true);
      notify(message, true);
    }
    try {
      const probe=key+':probe';
      localStorage.setItem(probe,'ok');
      if(localStorage.getItem(probe)!=='ok')throw Error('storage denied');
      localStorage.removeItem(probe);
      priorRaw=localStorage.getItem(key);
      if(priorRaw!==null){
        const restored=JSON.parse(priorRaw);
        if(!valid(restored))throw Error('persisted evidence is invalid');
        state=restored;
      }
    } catch (_) { lock('Attempt storage is unavailable or evidence is invalid. Nothing can be revealed or recorded.'); return; }
    function put(next) {
      try {
        if(localStorage.getItem(key)!==priorRaw){lock('Another tab changed this attempt. Reload to see the original saved evidence.');return false;}
        const raw=JSON.stringify(next);
        localStorage.setItem(key,raw);
        if(localStorage.getItem(key)!==raw)throw Error('readback mismatch');
        priorRaw=raw;state=next;render();return true;
      } catch (_) {lock('Attempt could not be saved and verified. Reconstruction remains protected.');return false;}
    }
    function commit(field, value) {
      if(!nonblank(value)){notify('Write a nonblank response before continuing.',true);return;}
      if(field==='firstAttempt' && !state.prediction){notify('Commit your prediction first.',true);return;}
      if(field==='diagnosis' && !state.firstAttempt){notify('Commit an attempt first.',true);return;}
      if(field==='repair' && !state.diagnosis){notify('Record your diagnosis first.',true);return;}
      if(field==='transfer' && !state.repair){notify('Record your repair first.',true);return;}
      if(state[field]){notify('This original response is already frozen.',true);return;}
      const next=JSON.parse(JSON.stringify(state));
      next[field]=field==='firstAttempt'?{text:value, helpBeforeAttempt:Object.keys(next.hints).sort()}:value;
      next.events.push({type:'COMMIT_'+field.toUpperCase(),at:new Date().toISOString()});
      put(next);
    }
    function render() {
      by('prediction-input').value=state.prediction||by('prediction-input').value;
      by('attempt-input').value=state.firstAttempt?.text||by('attempt-input').value;
      by('diagnosis-input').value=state.diagnosis||by('diagnosis-input').value;
      by('repair-input').value=state.repair||by('repair-input').value;
      by('transfer-input').value=state.transfer||by('transfer-input').value;
      for(const field of ['prediction','firstAttempt','diagnosis','repair','transfer']){
        by('save-'+field).disabled=!!state[field];
      }
      const reveal=!!state.firstAttempt;
      by('model-host').hidden=!reveal;
      if(reveal && !by('model-host').dataset.rendered){
        const list=document.createElement('ol');
        for(const step of data.route){
          const li=document.createElement('li');
          li.textContent=step.ask+' — '+step.step_answer;
          list.appendChild(li);
        }
        by('model-host').appendChild(list);
        by('model-host').dataset.rendered='yes';
      }
      by('diagnosis-stage').hidden=!reveal;
      by('repair-stage').hidden=!state.diagnosis;
      by('transfer-stage').hidden=!state.repair;
      by('boundary-answer').hidden=!state.transfer;
      if(state.transfer) by('boundary-answer').textContent=data.boundaryAnswer;
      root.querySelectorAll('[data-hint]').forEach(button => {
        const tier=button.dataset.hint;
        button.disabled=!!state.hints[tier];
        if(state.hints[tier]){
          const span=root.querySelector('[data-hint-text="'+tier+'"]');
          span.textContent=data.hints[Number(tier)-1];
        }
      });
      notify(reveal?'First answer saved and frozen. Reconstruction available.':'Prediction and original response are stored separately from hints and repairs.');
    }
    for(const field of ['prediction','firstAttempt','diagnosis','repair','transfer']){
      by('save-'+field).addEventListener('click',()=>commit(field,by(field+'-input').value));
    }
    root.querySelectorAll('[data-hint]').forEach(btn=>btn.addEventListener('click',()=>{
      const tier=btn.dataset.hint;
      if(state.hints[tier])return;
      const next=JSON.parse(JSON.stringify(state));
      next.hints[tier]={at:new Date().toISOString(),beforeAttempt:!state.firstAttempt};
      next.events.push({type:'HINT_EXPOSED',tier,at:next.hints[tier].at,beforeAttempt:!state.firstAttempt});
      put(next);
    }));
    window.addEventListener('storage',event=>{
      if(event.key===key && event.newValue!==priorRaw)lock('Another tab changed this evidence. Reload before continuing.');
    });
    render();
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);
  else boot();
})();
"""


def render_protected_core1b(original_html: str, b: dict) -> str:
    """Replace only Core1B panel; leave Core2 answer, navigation and source intact."""
    finder = _Core1BPanelFinder(original_html)
    finder.feed(original_html)
    if finder.start is None or finder.end is None:
        raise ValueError("No parseable Core1B panel; refusing unsafe HTML rewrite")
    stages = b["stages"]
    prompt = stages["stage_2_attempt"]["prompt"]
    prediction = stages["stage_1_predict"]["prompt"]
    boundary = stages["stage_6_boundary_test"]["prompt"]
    hints = [h["text"] for h in b["progressive_hints"]]
    if len(hints) != 3:
        raise ValueError("Three non-revealing hint tiers required")
    revision = hashlib.sha256(json.dumps(b, sort_keys=True).encode()).hexdigest()
    escape = lambda v: html.escape(str(v), quote=True)
    keyattrs = (
        f'data-source-id="{escape(b["target_question_id"])}" '
        f'data-practice-id="{escape(b["fresh_context_ref"])}" '
        f'data-revision="{revision}"'
    )
    inner = [
        f'<div id="content-core1b" class="tab-content" data-agent-b-core1b {keyattrs}>',
        '<style>#content-core1b [hidden]{display:none !important;} #content-core1b textarea{width:100%;min-height:5rem;} #content-core1b button{min-height:44px;margin:.35rem;}</style>',
        '<h2>Core 1B — New reconstruction practice</h2>',
        '<p>Source-distinct practice only. Your first response is not graded and remains unchanged after help.</p>',
        f'<section><h3>Stage 1 — Predict</h3><p>{escape(prediction)}</p><label for="ab-pred">Your physical prediction</label><textarea id="ab-pred" data-role="prediction-input"></textarea><button type="button" data-role="save-prediction">Save prediction</button></section>',
        f'<section><h3>Stage 2 — Independent attempt</h3><p>{escape(prompt)}</p><label for="ab-attempt">Your original calculation and model</label><textarea id="ab-attempt" data-role="firstAttempt-input"></textarea><button type="button" data-role="save-firstAttempt">Freeze original attempt</button></section>',
        '<section><h3>Optional H1/H2/H3 help</h3>',
    ]
    for i in (1, 2, 3):
        inner.append(f'<button type="button" data-hint="{i}">Reveal H{i} (record exposure)</button><p data-hint-text="{i}"></p>')
    inner.extend([
        '</section>',
        '<section data-role="model-host" hidden><h3>Stage 3 — Reconstruct after first commitment</h3></section>',
        '<section data-role="diagnosis-stage" hidden><h3>Stage 4 — Diagnose your first divergence</h3><textarea data-role="diagnosis-input" aria-label="Diagnose original model"></textarea><button type="button" data-role="save-diagnosis">Save diagnosis</button></section>',
        '<section data-role="repair-stage" hidden><h3>Stage 5 — Repair separately</h3><textarea data-role="repair-input" aria-label="Repair original model"></textarea><button type="button" data-role="save-repair">Save repair</button></section>',
        f'<section data-role="transfer-stage" hidden><h3>Stage 6 — Changed-condition transfer</h3><p>{escape(boundary)}</p><textarea data-role="transfer-input" aria-label="New changed-condition commitment"></textarea><button type="button" data-role="save-transfer">Save transfer response</button><p data-role="boundary-answer" hidden></p></section>',
        '<p data-role="status" aria-live="polite"></p></div>',
    ])
    payload = {
        "route": stages["stage_3_reconstruct"]["route"],
        "hints": hints,
        "boundaryAnswer": stages["stage_6_boundary_test"]["answer"],
    }
    raw = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
    replacement = "\n".join(inner)
    output = original_html[:finder.start] + replacement + original_html[finder.end:]
    script = '<script type="application/json" id="agent-b-core1b-data">'+raw+'</script>\n<script>'+ENGINE_JS.replace("</", "<\\/")+'</script>\n'
    if "</body>" not in output:
        raise ValueError("Cannot find end of generated learner page")
    return output.replace("</body>", script+"</body>", 1)
