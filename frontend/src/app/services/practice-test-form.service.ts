import { Injectable } from '@angular/core';
import { FormBuilder, FormGroup, FormArray, Validators } from '@angular/forms';

@Injectable({
  providedIn: 'root'
})
export class PracticeTestFormService {
  form: FormGroup;



  // We gon inject the form builder service into input
  constructor(private fb: FormBuilder) {
    this.form = this.fb.group({
      material: this.fb.array([], Validators.required),
      prompt: ['', Validators.required],
      formats: this.fb.array([], Validators.required)
    });
  }
  getForm(): FormGroup {
    return this.form;
  }
  get formats(): FormArray {
    return this.form.get('formats') as FormArray;
  }

  toggleFormat(format: string) {
    const formats = this.form.get('formats') as FormArray;
    const index = formats.value.indexOf(format);
    if (index === -1) {
      formats.push(this.fb.control(format));
    } else {
      formats.removeAt(index)
    }
  }

  resetForm() {
    this.form.reset();
    this.form.setControl('formats', this.fb.array([]));
  }
}


