@function rem($value) {
    @return unquote(($value/1px)/16 + "rem");
}

@media (max-width:992px) {
    .mobileMenu{
        position: fixed;
        top: 0;
        bottom: 0;
        margin: auto;
    }
}