#include <Python.h>

#include <otpgen/TokenDatabase.hpp>
#include <otpgen/TokenStore.hpp>

static TokenStore::TokenList tokenList{};

static PyObject *setTokenFile(PyObject *self, PyObject *args)
{
    const char *path;

    if (!PyArg_ParseTuple(args, "s", &path))
    {
        return nullptr;
    }

    return PyBool_FromLong(TokenDatabase::setTokenFile(path));
}

static PyObject *setPassword(PyObject *self, PyObject *args)
{
    const char *pass;

    if (!PyArg_ParseTuple(args, "s", &pass))
    {
        return nullptr;
    }

    return PyBool_FromLong(TokenDatabase::setPassword(pass));
}

static PyObject *loadTokens(PyObject *self, PyObject *args)
{
    const auto res = TokenDatabase::loadTokens();
    tokenList = TokenStore::i()->tokens();
    return Py_BuildValue("i", res);
}

static PyObject *getTokens(PyObject *self, PyObject *args)
{
    PyObject *py_list = PyList_New(tokenList.size());
    for (auto i = 0U; i < tokenList.size(); ++i)
    {
        const auto icon = reinterpret_cast<unsigned const char*>(tokenList.at(i)->icon().data());
        const auto dict = Py_BuildValue("{s:i,s:s,s:y#}",
            "index", i,
            "label", tokenList.at(i)->label().c_str(),
            "icon", icon, tokenList.at(i)->icon().size());
        PyList_SetItem(py_list, i, dict);
    }

    return py_list;
}

static PyObject *generateToken(PyObject *self, PyObject *args)
{
    unsigned int index = 0;

    if (!PyArg_ParseTuple(args, "I", &index))
    {
        return nullptr;
    }

    // out of bound
    if (index >= tokenList.size())
    {
        return Py_None;
    }

    return Py_BuildValue("s", tokenList.at(index)->generateToken().c_str());
}

static PyMethodDef otpgenpy_methods[] = {
    {"setTokenFile",  setTokenFile,  METH_VARARGS, nullptr},
    {"setPassword",   setPassword,   METH_VARARGS, nullptr},
    {"loadTokens",    loadTokens,    METH_VARARGS, nullptr},
    {"getTokens",     getTokens,     METH_VARARGS, nullptr},
    {"generateToken", generateToken, METH_VARARGS, nullptr},

    {nullptr, nullptr, 0, nullptr},
};

static struct PyModuleDef otpgenpy_module = {
    PyModuleDef_HEAD_INIT,
    "otpgenpy", // module name
    nullptr,    // module documentation
    -1,
    otpgenpy_methods,
};

PyMODINIT_FUNC PyInit_libotpgenpy(void)
{
    return PyModule_Create(&otpgenpy_module);
}
