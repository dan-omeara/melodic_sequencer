\version "2.24.3" 

\language "english"

#(set-global-staff-size 20)
diatonicScale = \relative {
c'8 d e f g a b
}
motif = \relative {
c'8 ( d e b )
}

\new Staff{
\key c \major
\transpose c c {
\modalTranspose c c \diatonicScale \motif 
\modalTranspose c d \diatonicScale \motif 
\modalTranspose c e \diatonicScale \motif 
\modalTranspose c f \diatonicScale \motif 
\modalTranspose c g \diatonicScale \motif 
\modalTranspose c a \diatonicScale \motif 

}}
\new Staff{
\key g \major
\transpose c g {
\modalTranspose c c \diatonicScale \motif 
\modalTranspose c d \diatonicScale \motif 
\modalTranspose c e \diatonicScale \motif 
\modalTranspose c f \diatonicScale \motif 
\modalTranspose c g \diatonicScale \motif 
\modalTranspose c a \diatonicScale \motif 

}}
\new Staff{
\key d \major
\transpose c d {
\modalTranspose c c \diatonicScale \motif 
\modalTranspose c d \diatonicScale \motif 
\modalTranspose c e \diatonicScale \motif 
\modalTranspose c f \diatonicScale \motif 
\modalTranspose c g \diatonicScale \motif 
\modalTranspose c a \diatonicScale \motif 

}}
\new Staff{
\key a \major
\transpose c a {
\modalTranspose c c \diatonicScale \motif 
\modalTranspose c d \diatonicScale \motif 
\modalTranspose c e \diatonicScale \motif 
\modalTranspose c f \diatonicScale \motif 
\modalTranspose c g \diatonicScale \motif 
\modalTranspose c a \diatonicScale \motif 

}}
\new Staff{
\key e \major
\transpose c e {
\modalTranspose c c \diatonicScale \motif 
\modalTranspose c d \diatonicScale \motif 
\modalTranspose c e \diatonicScale \motif 
\modalTranspose c f \diatonicScale \motif 
\modalTranspose c g \diatonicScale \motif 
\modalTranspose c a \diatonicScale \motif 

}}
\new Staff{
\key b \major
\transpose c b {
\modalTranspose c c \diatonicScale \motif 
\modalTranspose c d \diatonicScale \motif 
\modalTranspose c e \diatonicScale \motif 
\modalTranspose c f \diatonicScale \motif 
\modalTranspose c g \diatonicScale \motif 
\modalTranspose c a \diatonicScale \motif 

}}
\new Staff{
\key gf \major
\transpose c gf {
\modalTranspose c c \diatonicScale \motif 
\modalTranspose c d \diatonicScale \motif 
\modalTranspose c e \diatonicScale \motif 
\modalTranspose c f \diatonicScale \motif 
\modalTranspose c g \diatonicScale \motif 
\modalTranspose c a \diatonicScale \motif 

}}
\new Staff{
\key df \major
\transpose c df {
\modalTranspose c c \diatonicScale \motif 
\modalTranspose c d \diatonicScale \motif 
\modalTranspose c e \diatonicScale \motif 
\modalTranspose c f \diatonicScale \motif 
\modalTranspose c g \diatonicScale \motif 
\modalTranspose c a \diatonicScale \motif 

}}
\new Staff{
\key af \major
\transpose c af {
\modalTranspose c c \diatonicScale \motif 
\modalTranspose c d \diatonicScale \motif 
\modalTranspose c e \diatonicScale \motif 
\modalTranspose c f \diatonicScale \motif 
\modalTranspose c g \diatonicScale \motif 
\modalTranspose c a \diatonicScale \motif 

}}
\new Staff{
\key ef \major
\transpose c ef {
\modalTranspose c c \diatonicScale \motif 
\modalTranspose c d \diatonicScale \motif 
\modalTranspose c e \diatonicScale \motif 
\modalTranspose c f \diatonicScale \motif 
\modalTranspose c g \diatonicScale \motif 
\modalTranspose c a \diatonicScale \motif 

}}
\new Staff{
\key bf \major
\transpose c bf {
\modalTranspose c c \diatonicScale \motif 
\modalTranspose c d \diatonicScale \motif 
\modalTranspose c e \diatonicScale \motif 
\modalTranspose c f \diatonicScale \motif 
\modalTranspose c g \diatonicScale \motif 
\modalTranspose c a \diatonicScale \motif 

}}
\new Staff{
\key f \major
\transpose c f {
\modalTranspose c c \diatonicScale \motif 
\modalTranspose c d \diatonicScale \motif 
\modalTranspose c e \diatonicScale \motif 
\modalTranspose c f \diatonicScale \motif 
\modalTranspose c g \diatonicScale \motif 
\modalTranspose c a \diatonicScale \motif 

}}