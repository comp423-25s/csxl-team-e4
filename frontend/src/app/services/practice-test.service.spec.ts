import { TestBed } from '@angular/core/testing';

import { PracticeTestService } from './practice-test.service';

describe('PracticeTestService', () => {
  let service: PracticeTestService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PracticeTestService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
