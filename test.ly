\version "2.24.3"

#(set-global-staff-size 17)
global = {
    \time 4/4
    \key c \major
    \numericTimeSignature
}
melody = \relative {
  \global

\tuplet 5/4 { c'8 d e a g d e f b a e f g c b f g a d c g a b e d a b c f e b c d g f }
}

\score {
  <<
    \new Staff  {
      \context Voice = "vocal" { \melody }
    }
  >>
}
