# Real-Time-Ultrasound-Imaging-Feedback

This repository has been created for my semester project at <a href="https://arsl.ethz.ch/">ARSL</a> with <a href="https://arsl.ethz.ch/the-group/ProfAhmed.html">Prof. Daniel Ahmed</a> and <a href="https://mavt.ethz.ch/people/person-detail.Mjg4Mzc2.TGlzdC81NTksLTE3MDY5NzgwMTc=.html">Mahmoud Medany</a>. The purpose of the project is to build a real-time ultrasound imaging feedback in order to control microbubbles to a specific location.

## Setup
<p align="center">
  <img src="https://github.com/LilianLaporte/Real-Time-Ultrasound-Imaging-Feedback/assets/93781819/d2da1b19-8944-4e53-b000-feccf9a6a733" alt="Setup" width="80%"/>
</p>

## Feedback system

### Tracker pipeline
The initial stage of the pipeline involves implementing anatomical filtering to identify the channels (in both parallel and perpendicular cross-sections). Following this, the tracker integrates microbubble detection using template matching and employs [DeepSORT](https://github.com/nwojke/deep_sort) to determine the positions of the bounding boxes.
<p align="center">
  <img src="https://github.com/LilianLaporte/Real-Time-Ultrasound-Imaging-Feedback/assets/93781819/31517762-7837-4706-aebb-da512fc483cc" alt="Pipeline" width="80%"/>
</p>

### Output
<p align="center">
  <img src="https://github.com/LilianLaporte/Real-Time-Ultrasound-Imaging-Feedback/assets/93781819/b7a52344-ac57-4b1d-8cf0-2fdb64fb10b9" alt="Tracker" width="50%"/>
</p>

## Control using ultrasound
Ultrasound waves enable the control of microbubbles, allowing their trajectory to be manipulated even under specific flow conditions.
<p align="center">
  <img src="https://github.com/LilianLaporte/Real-Time-Ultrasound-Imaging-Feedback/assets/93781819/31672eda-28bb-4878-b5a7-6eea33aff838" alt="Control" width="50%"/>
</p>
