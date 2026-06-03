import { TestBed } from '@angular/core/testing';

import { ManualReview } from './manual-review';

describe('ManualReview', () => {
  let service: ManualReview;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ManualReview);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
