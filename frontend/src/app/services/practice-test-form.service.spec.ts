import { TestBed } from '@angular/core/testing';

import { PracticeTestFormService } from './practice-test-form.service';

describe('PracticeTestFormService', () => {
  let service: PracticeTestFormService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PracticeTestFormService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
