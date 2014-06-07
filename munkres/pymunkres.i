%module(directors="1") pymunkres

%include "stl.i"
%include "std_vector.i"
%include "std_pair.i"
%include "std_string.i"

//%include "typemaps.i"
%include "cpointer.i"

%include "exception.i"

%{
#define SWIG_FILE_WITH_INIT
%}


%include "numpy.i"

%exception {
  try {
    $action
  } catch (const std::exception& e) {
    SWIG_exception(SWIG_RuntimeError, e.what());
  }
}

%init %{
    import_array();
%}

%apply (double* INPLACE_ARRAY2, int DIM1, int DIM2) {(double* data_array, int nrows, int ncols)}


// This should include all necessary header files
%{
#include "munkresheaders.h"
%}

%include "matrix.hpp"
%include "munkres.h"

