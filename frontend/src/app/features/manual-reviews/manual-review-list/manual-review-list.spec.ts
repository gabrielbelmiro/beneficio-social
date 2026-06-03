import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManualReviewList } from './manual-review-list';

describe('ManualReviewList', () => {
  let component: ManualReviewList;
  let fixture: ComponentFixture<ManualReviewList>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ManualReviewList],
    }).compileComponents();

    fixture = TestBed.createComponent(ManualReviewList);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
